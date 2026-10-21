from django.db import connection


class Log:
    def __init__(self, id, date, description, id_user, module):
        self.id = id
        self.date = date
        self.description = description
        self.id_user = id_user
        self.module = module


    @classmethod
    def get_all(cls) -> list["Log"]:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT `id`, `date`, `description`, `id_user`, `module` FROM `log`"
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3], row[4])
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
