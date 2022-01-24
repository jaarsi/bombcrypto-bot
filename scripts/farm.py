import os
import asyncio
import pyautogui as pag
import logging

LOG_FILE = "farm.log"
INSTANCES_PER_COL = int(os.getenv("INSTANCES_PER_COL", 1))
INSTANCES_PER_ROW = int(os.getenv("INSTANCES_PER_ROW", 1))
INSTANCE_PROCESSING_MAX_ATTEMPTS = int(os.getenv("INSTANCE_PROCESSING_MAX_ATTEMPTS", 1))
SEARCH_ASSET_MAX_ATTEMPTS = int(os.getenv("SEARCH_ASSET_MAX_ATTEMPTS", 3))
SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS = int(os.getenv("SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS", 5))
FF_REFRESH_PAGE = "images/ff_refresh_page.png"
BC_CONNECT_WALLET = "images/bc_connect_wallet.png"
MM_SIGN_REQUEST = "images/mm_sign_request.png"
BC_SHOW_HEROES = "images/bc_show_heroes.png"
BC_SHOW_HEROES_WORK_ALL = "images/bc_show_heroes_work_all.png"
BC_SHOW_HEROES_CLOSE = "images/bc_show_heroes_close.png"
BC_START_TREASURE_HUNT = "images/bc_start_treasure_hunt.png"
BC_TREASURE_HUNT_CLOSE = "images/bc_treasure_hunt_close.png"
BC_ERROR_MESSAGE = "images/bc_error_message.png"
FF_BOMBCRYPTO = "images/ff_bombcrypto.png"

logging.basicConfig(
    filename=LOG_FILE,
    encoding='utf-8',
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def _search_and_click(region, asset, description, confidence, attempt=1):
    p = pag.locateCenterOnScreen(asset, confidence=confidence, region=region)
    logging.info( f"Region {region}: Searching for '{description}' => Get position {p} #{attempt}")

    if not p:
        return False

    pag.click(p.x, p.y)
    return True

async def search_and_click(region, asset, description, confidence=.9):
    attempt = 0

    while (attempt  < SEARCH_ASSET_MAX_ATTEMPTS):
        attempt += 1

        if not (await _search_and_click(region, asset, description, confidence, attempt)):
            await asyncio.sleep(SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS)
            continue

        return True

    return False

async def _process_region(region, attempt=1):
    if not (await search_and_click(region, FF_BOMBCRYPTO, f"enter bombcrypto #{attempt}")):
        return False

    await asyncio.sleep(10)

    if not (await search_and_click(region, BC_CONNECT_WALLET, f"connect wallet #{attempt}")):
        return False

    await asyncio.sleep(10)

    if not (await search_and_click(None, MM_SIGN_REQUEST, f"sign metamask #{attempt}")):
        return False

    await asyncio.sleep(20)

    if not (await search_and_click(region, BC_SHOW_HEROES, f"show heroes #{attempt}")):
        return False

    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES_WORK_ALL, f"work all #{attempt}", .6)
    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES_CLOSE, f"close heroes menu #{attempt}")
    await asyncio.sleep(3)

    if not (await search_and_click(region, BC_START_TREASURE_HUNT, f"start treasure hunt #{attempt}")):
        return False

async def process_region(region):
    attempt = 0

    while attempt < INSTANCE_PROCESSING_MAX_ATTEMPTS:
        attempt += 1

        if not (await _process_region(region, attempt)):
            continue

        break

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
    jobs = [ process_region(region) for region in regions ]
    return await asyncio.gather(*jobs)

if __name__ == "__main__":
    logging.info("[Starting]")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.warning("[Interrupted]")
    except Exception as e:
        logging.error(str(e))
    else:
        logging.info("[Finished]")
