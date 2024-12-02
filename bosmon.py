import sys
import re
import aiohttp
import asyncio
from enum import Enum
from time import gmtime, strftime

pattern = r"POCSAG1200:\s+Address:\s+(\d+)\s+Function:\s+(\d)"
VALUES=['a','b','c','d']

URL=sys.argv[1]
ENDPOINT=sys.argv[2]
USERNAME=sys.argv[3]
PASSWORD=sys.argv[4]

async def publish(addr: str, func: str, type: str = 'pocsag'):
        try:
                async with aiohttp.ClientSession() as websession:
                        async with websession.post(f'{URL}/telegramin/{ENDPOINT}/input.xml', data={
                                'type': type,
                                'address': addr,
                                'function': func
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
                addr = result[1].rjust(7, '0')
                key = result[2]
                func = VALUES[int(key)]
                local_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                
                print(f"{local_time}: RIC {addr} {func}")
                asyncio.run(publish(addr, func))
