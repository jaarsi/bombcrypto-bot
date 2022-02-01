import asyncio
from app import consts, core

async def farm_stop(region, wait_before_start):
    await asyncio.sleep(wait_before_start)
    core.search_and_click(region, consts.BC_TREASURE_HUNT_CLOSE, consts.INSTANCE_ASSET_CONFIDENCE)
    await asyncio.sleep(3)
    core.search_and_click(region, consts.BC_HEROES_MENU_OPEN, consts.INSTANCE_ASSET_CONFIDENCE)
    await asyncio.sleep(3)
    core.search_and_click(region, consts.BC_HEROES_MENU_REST_ALL, consts.INSTANCE_ASSET_CONFIDENCE)
    await asyncio.sleep(3)
    core.search_and_click(region, consts.FF_BOMBCRYPTO_CLOSE, consts.INSTANCE_ASSET_CONFIDENCE)

async def main():
    jobs = [ farm_stop(region, i*5) for i, region in enumerate(core.get_screen_regions(), 0) ]
    return await asyncio.gather(*jobs)

if __name__ == "__main__":
    asyncio.run(main())