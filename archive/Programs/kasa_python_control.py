#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 12:11:04 2024

@author: carterfox

Need to be on the devices network to control it like this. Everything needs to happen in the async function
"""

import asyncio
from kasa import Discover#, Credentials
import time

import nest_asyncio
nest_asyncio.apply()

async def main():
    dev = await Discover.discover_single("192.168.0.1",username="tairanxi0413@gmail.com",password="123Zhimakaimen")
    await dev.turn_off()
    await dev.update()
    print(dev.is_on)
    # time.sleep(2)
    # await dev.turn_off()
# 
if __name__ == "__main__":
    asyncio.run(main())


