import os

INSTANCES_PER_COL = int(os.getenv("INSTANCES_PER_COL", 1))
INSTANCES_PER_ROW = int(os.getenv("INSTANCES_PER_ROW", 1))
INSTANCE_PROCESSING_MAX_ATTEMPTS = int(os.getenv("INSTANCE_PROCESSING_MAX_ATTEMPTS", 1))
INSTANCE_FARMING_MAX_TIME = int(os.getenv("INSTANCE_FARMING_MAX_TIME", 1800))
INSTANCE_ASSET_CONFIDENCE = float(os.getenv("INSTANCE_ASSET_CONFIDENCE", .8))
SEARCH_ASSET_MAX_ATTEMPTS = int(os.getenv("SEARCH_ASSET_MAX_ATTEMPTS", 3))
SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS = int(os.getenv("SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS", 5))
FF_REFRESH_PAGE = "images/ff_refresh_page.png"
FF_BOMBCRYPTO_START = "images/ff_bombcrypto_start.png"
FF_BOMBCRYPTO_CLOSE = "images/ff_bombcrypto_close.png"
MM_SIGN_REQUEST = "images/mm_sign_request.png"
MM_CANCEL_SIGN = "images/mm_cancel_sign.png"
BC_CONNECT_WALLET = "images/bc_connect_wallet.png"
BC_CONNECT_WALLET2 = "images/bc_connect_wallet2.png"
BC_HEROES_MENU_OPEN = "images/bc_heroes_menu_open.png"
BC_HEROES_MENU_WORK_ALL = "images/bc_heroes_menu_work_all.png"
BC_HEROES_MENU_REST_ALL = "images/bc_heroes_menu_rest_all.png"
BC_HEROES_MENU_CLOSE = "images/bc_heroes_menu_close.png"
BC_TREASURE_HUNT_START = "images/bc_treasure_hunt_start.png"
BC_TREASURE_HUNT_CLOSE = "images/bc_treasure_hunt_close.png"
BC_ERROR_MESSAGE = "images/bc_error_message.png"
