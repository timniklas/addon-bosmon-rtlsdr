import sys
import re
import aiohttp
import asyncio
from enum import Enum

pattern = r"POCSAG1200:\s+Address:\s+(\d+)\s+Function:\s+(\d)"
VALUES=['a','b','c','d']

URL=sys.argv[1]
ENDPOINT=sys.argv[2]
USERNAME=sys.argv[3]
PASSWORD=sys.argv[4]

async def publish(address: str, func: str):
        try:
                async with aiohttp.ClientSession() as websession:
                        async with websession.post(f'{URL}/telegramin/{ENDPOINT}/input.xml', data={
                                'type': 'pocsag',
                                'address': address.rjust(7, '0'),
                                'function': VALUES[int(func)]
                        }, auth=aiohttp.BasicAuth(USERNAME, PASSWORD)) as response:
                                response.raise_for_status()
        except Exception as e:
                print(e)

for line in sys.stdin:
        if 'Exit' == line.rstrip():
                break
        if "No supported devices found." in line:
                break
        result = re.search(pattern, line)
        if result:
                print(f"{result[1]} {result[2]}")
                asyncio.run(publish(result[1], result[2]))