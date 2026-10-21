from django.db import connection

from ..enums.work_order_status import WorkOrderStatus


class WorkOrder:
    def __init__(
        self,
        title: str,
        description: str,
        status: WorkOrderStatus | int | str,
        id: int | None = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = WorkOrderStatus(int(status))


    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        status: WorkOrderStatus | int | str = WorkOrderStatus.PENDING,
    ) -> "WorkOrder":
        work_order_status = WorkOrderStatus(int(status))
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO work_order (title, description, status)
                VALUES (%s, %s, %s)
                """,
                [title, description, work_order_status.value],
            )
            work_order_id = cursor.lastrowid

        return cls(title, description, work_order_status, id=work_order_id)


    @classmethod
    def update(
        cls,
        order_id: int,
        title: str,
        description: str,
        status: WorkOrderStatus | int | str,
    ) -> None:
        work_order_status = WorkOrderStatus(int(status))
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE work_order 
                SET title = %s, description = %s, status = %s 
                WHERE id = %s
                """,
                [title, description, work_order_status.value, order_id],
            )


    @classmethod
    def get_all(cls) -> list["WorkOrder"]:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, description, status FROM work_order"
            )
            rows = cursor.fetchall()

        return [
            cls(title, description, status, id=work_order_id)
            for work_order_id, title, description, status in rows
        ]
