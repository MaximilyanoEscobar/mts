import asyncio
import traceback

from handlers.admin.admin_area import admin_router
from handlers.echo import echo_router
from handlers.user.key_menu import key_router
from handlers.user.number_menu import number_router
from handlers.user.personal_area import personal_area_router
from loader import dp, bots_list
from utils.message_middleware import MessageMiddleware


async def main() -> None:
    try:
        dp.message.middleware.register(MessageMiddleware())
        print((await bots_list[0].get_me()).full_name)
        dp.include_routers(admin_router, key_router, personal_area_router, number_router, echo_router)
        await dp.start_polling(*bots_list)
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    asyncio.run(main())
