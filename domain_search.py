import asyncio, socket, keyword

MAX_LEN = 4

async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop()                       #
    try:
        await loop.getaddrinfo(domain, None)                #
    except socket.gaierror:
        return domain, False
    return domain, True


async def main() -> None:
    names = (kw for kw in keyword.kwlist if len(kw) <= MAX_LEN)
    domains = (f'{name}.dev'.lower() for name in names)
    coros = [probe(domain) for domain in domains]           # list of coroutine objects
    # coros = (probe(domain) for domain in domains)           # list of coroutine objects
    for coro in asyncio.as_completed(coros):                # in the order coro is completed
        domain, found = await coro                          #
        mark = '+' if found else ' '
        print(f'{mark} {domain}')


if __name__ == '__main__':
    asyncio.run(main())                                     # event loop 시작, returns only when the event loop exits