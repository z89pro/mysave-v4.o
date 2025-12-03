from loguru import logger
import sys

# Reset logger to be clean
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")

def get_logger():
    return logger
