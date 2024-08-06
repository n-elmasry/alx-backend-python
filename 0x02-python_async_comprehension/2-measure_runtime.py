#!/usr/bin/env python3
"""measure_runtime"""

import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """will execute async_comprehension four times in parallel"""
    start_time = time.time()
    coroutines = [async_comprehension() for _ in range(4)]
    await asyncio.gather(*coroutines)
    return time.time() - start_time
