import sys
from logging import logger

logger.remove()
logger.add(sys.stdout, colorize=False, format="{time:YYYYMMDDHHmmss}|{level}| {message}")
