from django.db import connection

from ..enums.profile import Profile


class User:
    def __init__(self, name: str, account: str, profile: Profile | int, id: int | None = None):
        self.id = id
        self.name = name
        self.account = account
        self.profile = Profile(profile)

    def is_admin(self) -> bool:
        return self.profile == Profile.ADMINISTRADOR

    @staticmethod
    def get_all() -> list["User"]:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, account, profile FROM `user`")
            rows = cursor.fetchall()

        return [
            User(row[1], row[2], row[3], id=row[0])
            for row in rows
        ]

    @staticmethod
    def get_by_id(user_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, account, profile FROM `user` WHERE id = %s",
                [user_id]
            )
            row = cursor.fetchone()

        if row:
            return User(row[1], row[2], row[3], id=row[0])
        return None

    @staticmethod
    def login(account: str, password: str):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, account, profile FROM `user` WHERE account = %s AND password = %s",
                [account, password]
            )
            row = cursor.fetchone()

        if row:
            return User(row[1], row[2], row[3], id=row[0])
        return None

    @staticmethod
    def create(name: str, account: str, password: str, profile: int = 1):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO `user` (name, account, password, profile) VALUES (%s, %s, %s, %s)",
                [name, account, password, int(profile)]
            )
            user_id = cursor.lastrowid

        return User(name, account, int(profile), id=user_id)

