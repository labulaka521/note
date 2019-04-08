import asyncio
# 可等待对象
async def nested():
    return 42

async def main():
    nested()

    print(await nested())


async def main_task():
    task = asyncio.create_task(nested())
    await task

print(asyncio.run(main_task()))
