from django.db import connection

from ..enums.system_module import SystemModule


class Log:
    def __init__(self, id, date, description, id_user, module, user_name: str | None = None):
        self.id = id
        self.date = date
        self.description = description
        self.id_user = id_user
        self.module = SystemModule(int(module))
        self.user_name = user_name


    @classmethod
    def get_all(cls) -> list["Log"]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT l.id, l.date, l.description, l.id_user, l.module, u.name
                FROM `log` l
                LEFT JOIN `user` u ON l.id_user = u.id
                ORDER BY l.id DESC
                """
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3], row[4], user_name=row[5])
            for row in rows
        ]


    @classmethod
    def create(cls, description: str, id_user: int, module: int):
        """
        Inserta un nuevo registro de log en la base de datos con la hora actual (NOW()).
        """
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO `log` (`date`, `description`, `id_user`, `module`)
                VALUES (NOW(), %s, %s, %s)
                """,
                [description, id_user, module]
            )
