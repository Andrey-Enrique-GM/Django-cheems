from django.db import connection


class WorkOrderHistory:
    def __init__(self, date, id_user, action, id_work_order):
        self.date = date
        self.id_user = id_user
        self.action = action
        self.id_work_order = id_work_order

    @classmethod
    def get_all(cls) -> list["WorkOrderHistory"]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT date, id_user, action, id_work_order
                FROM work_order_history
                """
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3])
            for row in rows
        ]
