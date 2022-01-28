import os
import logging
import requests as rq

NR_LOG_ENDPOINT = os.getenv("NR_LOG_ENDPOINT")
NR_ENABLED = bool(os.getenv("NR_ENABLED", False))

def create_logger(name):
    class _NewRelicHandler(logging.Handler):
        def emit(self, record):
            asset_pos = getattr(record, "asset_pos", None)
            payload = {
                "region": getattr(record, "region", None),
                "asset_pos": asset_pos and repr(asset_pos),
                "process_attempt": getattr(record, "process_attempt", None),
                "search_attempt": getattr(record, "search_attempt", None),
                "message": record.message
            }

            try:
                rq.post(NR_LOG_ENDPOINT, json=payload)
            except:
                pass

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

    if NR_ENABLED:
        logger.addHandler(_NewRelicHandler())

    return logger
