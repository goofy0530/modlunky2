import struct
import time
import textwrap
from pathlib import Path
from .injectlib import Injector

DELTA = 0xc00

def signed(x):
    return x if x & 0x80000000 == 0 else x - 0x100000000

class ItemSpawner:
    def __init__(self, proc):
        with Path(proc.cmdline()[0]).open('rb') as proc_file:
            self.data = proc_file.read()

        self.proc = Injector(proc)
        self.base = self.proc.find_base('spel2.exe')
        self.main_thread = self.proc.threads()[0]

        _, self.state = self.find('83 78 0C 05 0F 85 ', -15)
        self.state = self.proc.r64(self.base + self.state)

        _, self.layer_off = self.find('C6 80 58 44 06 00 01 ', -7, 'imm')

        inst, _ = self.find('BA 88 02 00 00', 1, 'off')
        self.load_item, _ = self.find('BA 88 02 00 00', 8, 'off', start=inst)
        self.load_item += signed(struct.unpack_from("<L", self.data, self.load_item + 1)[0]) + 5
        self.load_item += DELTA
        self.load_item += self.base

        _, self.items_off = self.find('33 D2 8B 41 28 01', -7, 'imm')

    def find(self, sep, offset=-7, type='pc', start=0):
        off = self.data.find(bytes.fromhex(sep), start)
        if type == 'off':
            return off + offset, None
        inst = self.data[off + offset:off]
        off2, = struct.unpack_from("<L", inst, 3)
        if type == 'imm':
            gm = off2
        elif type == 'pc':
            gm = off + offset + 7 + off2 + DELTA
        return off + DELTA, gm

    def spawn(self, item_num):
        layer = self.proc.r64(self.state + self.layer_off)
        items = self.proc.r64(self.state + self.items_off)

        player_index = self.proc.r8(items)
        size = self.proc.r8(items + 1)
        player = self.proc.r64(items + 8 + player_index * 8)

        # Player X, Y
        
        x, y = struct.unpack("<2f", self.proc.read(player + 0x40, 8))
        x += 2

        #print(f"State: {self.state}, Layer Offset: {self.layer_off}, Load Item: {self.load_item}")
        #print(f"Layer: {layer}, Items: {items}, Player Index: {player_index}, Size: {size}, Player: {player}")
        
        self.proc.run(textwrap.dedent(rf"""
        import ctypes
        import sys
        import os

        def hook(name, *args):
            if name != 'ctypes.seh_exception':
                return
            os.system("cmd")

        sys.addaudithook(hook)

        class CriticalSection:
            def __enter__(self, *args):
                ctypes.windll.kernel32.SuspendThread({self.main_thread})

            def __exit__(self, *args):
                ctypes.windll.kernel32.ResumeThread({self.main_thread})
        try:
            with CriticalSection():
                load_item = (ctypes.CFUNCTYPE(ctypes.c_void_p,
                    ctypes.c_void_p,
                    ctypes.c_int64,
                    ctypes.c_float,
                    ctypes.c_float))({self.load_item})
                load_item({layer}, {item_num}, {x}, {y})
        except Exception as e:
            import os
            os.system("msg * \"%s\"" % e)
        """).strip().encode())