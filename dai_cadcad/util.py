""" Utility Module
    Contains utility functions such as those for raising exceptions.
"""


def require(cond, message):
    """ Simple method to raise an exception with the given `message`
        if `cond` evaluates to False.
    """

    if not cond:
        raise Exception(message)
