import logging
import pyautogui as pag
from random import randint
from . import consts

def create_logger(name):
    class _LoggerFormatter(logging.Formatter):
        def format(self, record) -> str:
            try:
                return super().format(record)
            except:
                return f"{record.asctime} => {record.message}"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    default_fmtr = _LoggerFormatter(
        "{asctime} => {region} {message} {asset_pos} {process_attempt} {search_attempt}",
        "%Y-%m-%d %H:%M:%S",
        style="{"
    )
    file_handler = logging.FileHandler(f"{name}.log", mode="w")
    file_handler.setFormatter(default_fmtr)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(default_fmtr)
    logger.addHandler(stream_handler)
    return logger

def search_and_click(region, asset, confidence):
    if not (p := pag.locateOnScreen(asset, confidence=confidence, region=region)):
        return None

    x, y = (
        p.left + randint(1, p.width-1),
        p.top + randint(1, p.height-1)
    )
    pag.click(x, y)
    return x, y

def get_screen_regions():
    ss = pag.size()
    return [
        (
            x*ss.width//consts.INSTANCES_PER_COL,
            y*ss.height//consts.INSTANCES_PER_ROW,
            ss.width//consts.INSTANCES_PER_COL,
            ss.height//consts.INSTANCES_PER_ROW
        )
        for x in range(consts.INSTANCES_PER_COL)
        for y in range(consts.INSTANCES_PER_ROW)
    ]