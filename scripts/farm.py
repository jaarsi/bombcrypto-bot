import os
import asyncio
from random import randint
import pyautogui as pag
import logging

LOG_FILE = "farm.log"
INSTANCES_PER_COL = int(os.getenv("INSTANCES_PER_COL", 1))
INSTANCES_PER_ROW = int(os.getenv("INSTANCES_PER_ROW", 1))
INSTANCE_PROCESSING_MAX_ATTEMPTS = int(os.getenv("INSTANCE_PROCESSING_MAX_ATTEMPTS", 1))
INSTANCE_FARMING_MAX_TIME = int(os.getenv("INSTANCE_FARMING_MAX_TIME", 1800))
INSTANCE_WAIT_BEFORE_START_FACTOR = int(os.getenv("INSTANCE_WAIT_BEFORE_START_FACTOR", 10))
INSTANCE_DEFAULT_CONFIDENCE = .8
SEARCH_ASSET_MAX_ATTEMPTS = int(os.getenv("SEARCH_ASSET_MAX_ATTEMPTS", 3))
SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS = int(os.getenv("SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS", 5))
FF_REFRESH_PAGE = "images/ff_refresh_page.png"
FF_BOMBCRYPTO = "images/ff_bombcrypto.png"
FF_HOME = "images/ff_home.png"
MM_SIGN_REQUEST = "images/mm_sign_request.png"
MM_CANCEL_SIGN = "images/mm_cancel_sign.png"
BC_CONNECT_WALLET = "images/bc_connect_wallet.png"
BC_SHOW_HEROES = "images/bc_show_heroes.png"
BC_SHOW_HEROES_WORK_ALL = "images/bc_show_heroes_work_all.png"
BC_SHOW_HEROES_REST_ALL = "images/bc_show_heroes_rest_all.png"
BC_SHOW_HEROES_CLOSE = "images/bc_show_heroes_close.png"
BC_START_TREASURE_HUNT = "images/bc_start_treasure_hunt.png"
BC_TREASURE_HUNT_CLOSE = "images/bc_treasure_hunt_close.png"
BC_ERROR_MESSAGE = "images/bc_error_message.png"

logging.basicConfig(
    # filename=LOG_FILE,
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s => %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def _search_and_click(region, asset, confidence):
    if not (p := pag.locateOnScreen(asset, confidence=confidence, region=region)):
        return None

    x, y = (
        p.left + randint(1, p.width-1),
        p.top + randint(1, p.height-1)
    )
    pag.click(x, y)
    return p, x, y

async def search_and_click(region, asset, description, confidence, process_attempt):
    attempt = 0

    while (attempt  < SEARCH_ASSET_MAX_ATTEMPTS):
        attempt += 1
        asset_pos = await _search_and_click(region, asset, confidence)
        logging.info(
            f"SEARCH FOR {description} ON REGION {repr(region)} GOT {asset_pos} {process_attempt}|{attempt}"
        )

        if not asset_pos:
            await asyncio.sleep(SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS)
            continue

        return True

    return False

async def _process_region(region, attempt):
    if not (await search_and_click(region, FF_BOMBCRYPTO, "ENTER BOMBCRYPTO", INSTANCE_DEFAULT_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(15)

    if not (await search_and_click(region, BC_CONNECT_WALLET, "CONNECT WALLET", INSTANCE_DEFAULT_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(15)

    if not (await search_and_click(None, MM_SIGN_REQUEST, "SIGN METAMASK", INSTANCE_DEFAULT_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(30)

    if not (await search_and_click(region, BC_SHOW_HEROES, "SHOW HEROES", INSTANCE_DEFAULT_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES_WORK_ALL, "WORK ALL", .6, attempt)
    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES_CLOSE, "CLOSE HEROES MENU", INSTANCE_DEFAULT_CONFIDENCE, attempt)
    await asyncio.sleep(3)

    if not (await search_and_click(region, BC_START_TREASURE_HUNT, "START TREASURE HUNT", INSTANCE_DEFAULT_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(INSTANCE_FARMING_MAX_TIME)
    await search_and_click(region, BC_TREASURE_HUNT_CLOSE, "CLOSE TREASURE HUNT", INSTANCE_DEFAULT_CONFIDENCE, attempt)
    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES, "SHOW HEROES", INSTANCE_DEFAULT_CONFIDENCE, attempt)
    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES_REST_ALL, "REST ALL", .6, attempt)
    await asyncio.sleep(3)
    await search_and_click(region, FF_HOME, "CLOSE BOMBCRYPTO", INSTANCE_DEFAULT_CONFIDENCE, attempt)
    return True

async def process_region(region, wait_before_start):
    await asyncio.sleep(wait_before_start)
    attempt = 0

    while attempt < INSTANCE_PROCESSING_MAX_ATTEMPTS:
        attempt += 1

        if not (await _process_region(region, attempt)):
            continue

        return True

    return False

async def main():
    ss = pag.size()
    regions = [
        (
            x*ss.width//INSTANCES_PER_COL,
            y*ss.height//INSTANCES_PER_ROW,
            ss.width//INSTANCES_PER_COL,
            ss.height//INSTANCES_PER_ROW
        )
        for x in range(INSTANCES_PER_COL)
        for y in range(INSTANCES_PER_ROW)
    ]
    jobs = [
        process_region(region, i*INSTANCE_WAIT_BEFORE_START_FACTOR)
        for i, region in enumerate(regions, 0)
    ]
    return await asyncio.gather(*jobs)

if __name__ == "__main__":
    logging.info("STARTING")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.warning("INTERRUPTED")
    except Exception as e:
        logging.error(str(e))
    else:
        logging.info("FINISHED")
