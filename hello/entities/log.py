from django.db import connection


class Log:
    def __init__(self, date, description, user, module):
        self.date = date
        self.description = description
        self.user = user
        self.module = module

    @classmethod
    def get_all(cls) -> list["Log"]:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT `date`, `description`, `user`, `module` FROM `log`"
            )
            rows = cursor.fetchall()

        return [
            cls(date, description, user, module)
            for date, description, user, module in rows
        ]
