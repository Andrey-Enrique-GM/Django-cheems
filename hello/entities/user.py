from django.db import connection

from ..enums.profile import Profile


class User:
    def __init__(self, name: str, account: str, profile: Profile | int):
        self.name = name
        self.account = account
        self.profile = Profile(profile)

    def is_admin(self) -> bool:
        return self.profile == Profile.ADMINISTRADOR

    @staticmethod
    def get_all() -> list["User"]:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, account, profile FROM `user`")
            rows = cursor.fetchall()

        return [
            User(row[0], row[1], row[2])
            for row in rows
        ]
