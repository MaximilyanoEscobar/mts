import asyncio
import traceback

from handlers.echo import echo_router
from handlers.user.check_number import check_number_router
from handlers.user.personal_area import personal_area_router
from loader import dp, bots_list
from utils.message_middleware import MessageMiddleware


async def main() -> None:
    try:
        dp.message.middleware.register(MessageMiddleware())
        print((await bots_list[0].get_me()).full_name)
        dp.include_routers(personal_area_router,check_number_router, echo_router)
        await dp.start_polling(*bots_list)
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    asyncio.run(main())
