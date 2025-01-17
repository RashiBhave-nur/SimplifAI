
# Standard imports
import logging


_logger = None
_handler = None

def setup_logger(verbose):
    global _logger
    global _handler

    if _logger is None:
        assert _handler is None

        # Create logger
        _logger = logging.getLogger('jira-bot')

    _logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Reset handler
    if _handler is not None:
        _logger.removeHandler(_handler)

    # Create console handler and set level to debug
    _handler = logging.StreamHandler()                            # NOTE Write everything to `stderr`!
    _handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(name)s[%(levelname)s]: %(message)s')
    _handler.setFormatter(formatter)

    # Add handler to logger
    _logger.addHandler(_handler)


def get_logger():
    global _logger
    assert _logger is not None, '`get_logger()` before `setup_logger()`! Code review required!'
    return _logger
