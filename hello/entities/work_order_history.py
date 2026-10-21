from django.db import connection

from ..enums.work_order_status import WorkOrderStatus


class WorkOrderHistory:
    def __init__(self, id, date, id_user, action, id_work_order, user_name: str | None = None):
        self.id = id
        self.date = date
        self.id_user = id_user
        self.action = WorkOrderStatus(int(action))
        self.id_work_order = id_work_order
        self.user_name = user_name


    @classmethod
    def get_all(cls) -> list["WorkOrderHistory"]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT woh.id, woh.date, woh.id_user, woh.action, woh.id_work_order, u.name
                FROM work_order_history woh
                LEFT JOIN `user` u ON woh.id_user = u.id
                ORDER BY woh.id DESC
                """
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3], row[4], user_name=row[5])
            for row in rows
        ]


    @classmethod
    def get_by_work_order(cls, work_order_id: int) -> list["WorkOrderHistory"]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT woh.id, woh.date, woh.id_user, woh.action, woh.id_work_order, u.name
                FROM work_order_history woh
                LEFT JOIN `user` u ON woh.id_user = u.id
                WHERE woh.id_work_order = %s
                ORDER BY woh.id DESC
                """,
                [work_order_id]
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3], row[4], user_name=row[5])
            for row in rows
        ]


    @classmethod
    def create(cls, id_user: int, action: int, id_work_order: int):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO work_order_history (date, id_user, action, id_work_order)
                VALUES (NOW(), %s, %s, %s)
                """,
                [id_user, action, id_work_order],
            )
