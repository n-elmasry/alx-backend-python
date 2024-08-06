#!/usr/bin/env python3
"""async_comprehension"""
import asyncio

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension():
    """ollect 10 random numbers using an async comprehensing over
    async_generator,then return the 10 random numbers."""
    random_nums = [number async for number in async_generator()]
    return random_nums
