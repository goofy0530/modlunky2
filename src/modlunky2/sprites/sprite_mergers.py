from .full_sheets import *


def get_all_sprite_mergers(base_path: str):
    return [
        CharacterBlackSpriteMerger(base_path),
        CharacterLimeSpriteMerger(base_path),
        CharacterMagentaSpriteMerger(base_path),
        CharacterOliveSpriteMerger(base_path),
        CharacterOrangeSpriteMerger(base_path),
        CharacterPinkSpriteMerger(base_path),
        CharacterRedSpriteMerger(base_path),
        CharacterVioletSpriteMerger(base_path),
        CharacterWhiteSpriteMerger(base_path),
        CharacterYellowSpriteMerger(base_path),
        CharacterBlueSpriteMerger(base_path),
        CharacterCeruleanSpriteMerger(base_path),
        CharacterCinnabarSpriteMerger(base_path),
        CharacterCyanSpriteMerger(base_path),
        CharacterGoldSpriteMerger(base_path),
        CharacterGraySpriteMerger(base_path),
        CharacterGreenSpriteMerger(base_path),
        CharacterIrisSpriteMerger(base_path),
        CharacterKhakiSpriteMerger(base_path),
        CharacterLemonSpriteMerger(base_path),
        CharacterEggChildSpriteMerger(base_path),
        CharacterHiredHandSpriteMerger(base_path),
        TurkeySpriteMerger(base_path),
        RockdogSpriteMerger(base_path),
        AxolotlSpriteMerger(base_path),
        QilinSpriteMerger(base_path),
        MontySpriteMerger(base_path),
        PercySpriteMerger(base_path),
        PoochiSpriteMerger(base_path),
    ]
