from django.db import connection


class Log:
    def __init__(self, date, description, id_user, module):
        self.date = date
        self.description = description
        self.id_user = id_user
        self.module = module

    @classmethod
    def get_all(cls) -> list["Log"]:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT `date`, `description`, `id_user`, `module` FROM `log`"
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3])
            for row in rows
        ]
