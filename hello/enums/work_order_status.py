from enum import IntEnum


class WorkOrderStatus(IntEnum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
