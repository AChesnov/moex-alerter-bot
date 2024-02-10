import logging
import os

from moex_alerter_bot.config import get_handler


def test_get_logging_without_file():
    assert os.getenv('LOG_FILE') is None
    assert isinstance(get_handler(), logging.StreamHandler)


def test_get_logging_with_file():
    log_file = 'test.log'
    assert os.getenv('LOG_FILE') is None
    os.environ['LOG_FILE'] = log_file
    assert os.getenv('LOG_FILE') == log_file
    assert isinstance(get_handler(), logging.FileHandler)
