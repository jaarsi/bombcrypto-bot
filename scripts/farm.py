import asyncio
from app import core, consts

logger = core.create_logger("farm")

async def search_and_click(region, asset, description, confidence, process_attempt):
    attempt = 0

    while (attempt  < consts.SEARCH_ASSET_MAX_ATTEMPTS):
        attempt += 1
        asset_pos = core.search_and_click(region, asset, confidence)
        logger.info(description, extra={
            "region": repr(region),
            "asset_pos": asset_pos,
            "process_attempt": process_attempt,
            "search_attempt": attempt
        })

        if not asset_pos:
            await asyncio.sleep(consts.SEARCH_ASSET_TIME_BETWEEN_ATTEMPTS)
            continue

        return True

    return False

async def _process_region(region, attempt):
    if not (await search_and_click(region, consts.FF_BOMBCRYPTO_START, "ENTER BOMBCRYPTO", consts.INSTANCE_ASSET_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(30)

    if not (await search_and_click(region, consts.BC_CONNECT_WALLET, "CONNECT WALLET", consts.INSTANCE_ASSET_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(3)

    if not (await search_and_click(region, consts.BC_CONNECT_WALLET2, "CONNECT WALLET2", consts.INSTANCE_ASSET_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(10)

    if not (await search_and_click(None, consts.MM_SIGN_REQUEST, "SIGN METAMASK", consts.INSTANCE_ASSET_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(60)

    if not (await search_and_click(region, consts.BC_HEROES_MENU_OPEN, "SHOW HEROES", consts.INSTANCE_ASSET_CONFIDENCE, attempt)):
        return False

    await asyncio.sleep(3)
    attempts = 0

    while (
        await search_and_click(region, consts.BC_HEROES_MENU_WORK_ALL, "WORK ALL", consts.INSTANCE_ASSET_CONFIDENCE, attempt)
        and attempts < 3
    ):
        attempts += 1

    await asyncio.sleep(3)
    await search_and_click(region, consts.BC_HEROES_MENU_CLOSE, "CLOSE HEROES MENU", consts.INSTANCE_ASSET_CONFIDENCE, attempt)
    await asyncio.sleep(3)

    if not (await search_and_click(region, consts.BC_TREASURE_HUNT_START, "START TREASURE HUNT", consts.INSTANCE_ASSET_CONFIDENCE, attempt)):
        return False

    return True

async def process_region(region, wait_before_start):
    await asyncio.sleep(wait_before_start)
    attempt = 0

    while attempt < consts.INSTANCE_PROCESSING_MAX_ATTEMPTS:
        attempt += 1

        if not (await _process_region(region, attempt)):
            continue

        return True

    await asyncio.sleep(3)
    await search_and_click(region, consts.FF_BOMBCRYPTO_CLOSE, "CLOSE BOMBCRYPTO", consts.INSTANCE_ASSET_CONFIDENCE, attempt)
    return False

async def main():
    jobs = [
	process_region(region, i*120)
	for i, region in enumerate(core.get_screen_regions(), 0)
    ]
    return await asyncio.gather(*jobs)

if __name__ == "__main__":
    logger.info("STARTING")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("INTERRUPTED")
    except Exception as e:
        logger.error(str(e))
    else:
        logger.info("FINISHED")
