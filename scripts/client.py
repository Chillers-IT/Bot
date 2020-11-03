from aiohttp import ClientSession
import asyncio


async def loop():
    async with ClientSession() as session:
        while True:
            message = input()
            async with session.post('http://0.0.0.0:8080', data=message.encode()) as response:
                answer = await response.text()
            print(answer)


if __name__ == '__main__':
    asyncio.run(loop())
