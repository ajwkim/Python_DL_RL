import time, asyncio


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(say_after(1, 'hello'))
        task2 = tg.create_task(say_after(2, 'world'))

        print(f'started at {time.strftime("%X")}')
    
    # await is implicit when the context manager exits          # runs corous concurrently

    print(f'finished at {time.strftime("%X")}')


asyncio.run(main())                             # total 2 sec.