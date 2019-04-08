import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)      # 等待一个协程
    print('word')

asyncio.run(main())     # 用来运行最高层级的入口点


