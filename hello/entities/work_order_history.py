from django.db import connection


class WorkOrderHistory:
    def __init__(self, date, user, action, work_order):
        self.date = date
        self.user = user
        self.action = action
        self.work_order = work_order

    @classmethod
    def get_all(cls) -> list["WorkOrderHistory"]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT `date`, `user`, `action`, `work_order`
                FROM `work_order_history`
                """
            )
            rows = cursor.fetchall()

        return [
            cls(date, user, action, work_order)
            for date, user, action, work_order in rows
        ]
