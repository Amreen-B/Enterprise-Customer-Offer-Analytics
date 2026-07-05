"""
============================================================
File : logger.py
Purpose : Central logging utility
============================================================
"""

import logging

def get_logger(name):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        logger.addHandler(console)

    return logger