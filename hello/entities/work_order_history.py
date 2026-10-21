from django.db import connection


class WorkOrderHistory:
    def __init__(self, id, date, id_user, action, id_work_order):
        self.id = id
        self.date = date
        self.id_user = id_user
        self.action = action
        self.id_work_order = id_work_order


    @classmethod
    def get_all(cls) -> list["WorkOrderHistory"]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, date, id_user, action, id_work_order
                FROM work_order_history
                ORDER BY id DESC
                """
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3], row[4])
            for row in rows
        ]


    @classmethod
    def get_by_work_order(cls, work_order_id: int) -> list["WorkOrderHistory"]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, date, id_user, action, id_work_order
                FROM work_order_history
                WHERE id_work_order = %s
                ORDER BY id DESC
                """,
                [work_order_id]
            )
            rows = cursor.fetchall()

        return [
            cls(row[0], row[1], row[2], row[3], row[4])
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
