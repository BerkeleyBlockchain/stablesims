""" Utility module.

Convenience functions like those for conversions between number representations and units.
"""
import math


def float_to_wad(val):
    """ Converts a float to a wad.
    """

    order = int(math.floor(math.log10(val)))
    max_precision_offset = max(16 - order, 0)
    max_precision_int = int(val * 10 ** max_precision_offset)
    return int(max_precision_int * 10 ** (18 - max_precision_offset))


def wad_to_float(wad):
    """ Converts a wad to a float.
    """

    return wad / 10 ** 18


def float_to_ray(val):
    """ Converts a float to a ray.
    """

    order = int(math.floor(math.log10(val)))
    max_precision_offset = max(16 - order, 0)
    max_precision_int = int(val * 10 ** max_precision_offset)
    return int(max_precision_int * 10 ** (27 - max_precision_offset))


def ray_to_float(ray):
    """ Converts a ray to a float.
    """

    return ray / 10 ** 27


def float_to_rad(val):
    """ Converts a float to a rad.
    """

    order = int(math.floor(math.log10(val)))
    max_precision_offset = max(16 - order, 0)
    max_precision_int = int(val * 10 ** max_precision_offset)
    return int(max_precision_int * 10 ** (45 - max_precision_offset))


def rad_to_float(rad):
    """ Converts a rad to a float.
    """

    return rad / 10 ** 45


def policy_reduce(policy_signal_dict_a, policy_signal_dict_b):
    """ Reduces policy signals by merging them into one dict.

        If there is an overlap in keys, the value of `policy_signal_dict_b` is taken.
    """

    return {**policy_signal_dict_a, **policy_signal_dict_b}
