from dotenv import load_dotenv

load_dotenv()

import os
import asyncio
import pyautogui as pag
import logging
from datetime import datetime

INSTANCES_PER_COL = int(os.getenv("INSTANCES_PER_COL", 1))
INSTANCES_PER_ROW = int(os.getenv("INSTANCES_PER_ROW", 1))
INSTANCES_WAIT_BETWEEN_PROCCESSING = int(os.getenv("INSTANCES_WAIT_BETWEEN_PROCCESSING", 60))
SEARCH_ASSET_MAX_TRIES = int(os.getenv("SEARCH_ASSET_MAX_TRIES", 3))
SEARCH_ASSET_TIME_BETWEEN_TRIES = int(os.getenv("SEARCH_ASSET_TIME_BETWEEN_TRIES", 5))
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
    filename='messages.log',
    encoding='utf-8',
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class EBCError(Exception):
    pass

async def search_and_click(region, asset, description, confidence=.9):
    tries = 0

    while (tries  < SEARCH_ASSET_MAX_TRIES):
        tries += 1
        p = pag.locateCenterOnScreen(asset, confidence=confidence, region=region)
        logging.info( f"{region}: Searching for '{description}' => Get position {p} #{tries}")

        if not p:
            await asyncio.sleep(SEARCH_ASSET_TIME_BETWEEN_TRIES)
            continue

        pag.click(p.x, p.y)
        break

async def process_region(region, wait_before_start):
    await asyncio.sleep(wait_before_start)
    await search_and_click(region, FF_BOMBCRYPTO, "enter bombcrypto")
    await asyncio.sleep(30)
    await search_and_click(region, BC_CONNECT_WALLET, "connect wallet")
    await asyncio.sleep(10)
    await search_and_click(None, MM_SIGN_REQUEST, "sign metamask")
    await asyncio.sleep(40)
    await search_and_click(region, BC_SHOW_HEROES, "show heroes")
    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES_WORK_ALL, "work all", .6)
    await asyncio.sleep(3)
    await search_and_click(region, BC_SHOW_HEROES_CLOSE, "close heroes menu")
    await asyncio.sleep(3)
    await search_and_click(region, BC_START_TREASURE_HUNT, "start treasure hunt")

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
    jobs = [ process_region(region, i*INSTANCES_WAIT_BETWEEN_PROCCESSING) for i, region in enumerate(regions, 0) ]
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
