#!/usr/bin/env python3
"""to_kv """
from typing import Union, Tuple


def to_kv(k: str, v: Union[float, int]) -> Tuple[str, float]:
    """returns a tuple"""
    return (k, float(v**2))
