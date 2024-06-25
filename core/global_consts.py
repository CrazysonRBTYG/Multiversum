# Игровые состояния
STATE_MAIN_MENU = 0
STATE_GAME = 1
STATE_COLLECTION = 2
STATE_SHOP = 3

GAME_NAME = "Multiversum"

CHAR_NORMIS = 0
CHAR_DIO_BRANDO = 1
CHAR_AKALI = 2
CHAR_GRINCH = 3

CHARACTERS = {CHAR_NORMIS: {"path": "core/view/assets/collection/characters/normis.png",
                            "banner-path": None,
                            "name": "Нормис",
                            "ability": [None, None, None]},
              CHAR_DIO_BRANDO: {"path": "core/view/assets/collection/characters/dio-brante.png",
                                "banner-path": None,
                                "name": "Дио Брандо",
                                "ability": [2000, 8, 30]},
              CHAR_AKALI: {"path": "core/view/assets/collection/characters/akali.png",
                           "banner-path": None,
                           "name": "Люк Скай",
                           "ability": [None, None, None]},
              CHAR_GRINCH: {"path": "core/view/assets/collection/characters/grinch.png",
                            "banner-path": "core/view/assets/shop/banners/grinch-banner.png",
                            "name": "Гринч",
                            "ability": [lambda val: val + round(val * 0.05), None, 25]}}

ABILITY_READY = 0
ABILITY_ON_CD = 1
ABILITY_ACTIVE = 2

SPIN_COST = 1000
GUARANTEED_SPINS_AMOUNT = 30

CURRENT_BANNER_CHAR = CHAR_GRINCH