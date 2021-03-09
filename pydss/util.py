""" Utility Module
    Contains utility functions such as those for raising exceptions.
"""


class RequireException(Exception):
    pass


def require(cond, message):
    """ Simple method to raise an exception with the given `message`
        if `cond` evaluates to False.
    """

    if not cond:
        raise RequireException(message)
