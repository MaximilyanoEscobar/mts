import asyncio
import traceback
from loader import dp, bots_list
from utils.message_middleware import MessageMiddleware


async def main() -> None:
    try:
        dp.message.middleware.register(MessageMiddleware())
        print((await bots_list[0].get_me()).full_name)
        dp.include_routers()
        await dp.start_polling(*bots_list)
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    asyncio.run(main())
