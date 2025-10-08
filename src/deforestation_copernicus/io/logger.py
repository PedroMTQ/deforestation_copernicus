import logging
import sys

from deforestation_copernicus.settings import DEBUG, LOGGER_PATH, SERVICE_NAME, __VERSION__

logger = logging.getLogger(SERVICE_NAME)
"""Logger object configured for this project/service"""
logger.propagate = False

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s")

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

local_handler = logging.StreamHandler(sys.stdout)
local_handler.setLevel(logging.DEBUG)
local_handler.setFormatter(formatter)

if LOGGER_PATH:
    file_handler = logging.FileHandler(LOGGER_PATH)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


logger.addHandler(local_handler)

if __VERSION__:
    logger.info(f'Deployed {SERVICE_NAME}:{__VERSION__}')


