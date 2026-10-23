from enum import IntEnum


class WorkOrderStatus(IntEnum):
    PENDIENTE = 1
    EN_PROGRESO = 2
    COMPLETADA = 3
