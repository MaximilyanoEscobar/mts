from domain.repository.admin import AdminsRepository


def is_admin(tg_id: int):
    admins_repo = AdminsRepository()
    admins_data = admins_repo.get_all()
    admins_list = admins_data.admins_list
    print(admins_list)
    return tg_id in admins_list