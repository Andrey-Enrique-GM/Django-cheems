import unittest
from unittest.mock import ANY, patch

from .entities.user import User
from .entities.work_order import WorkOrder
from .entities.work_order_history import WorkOrderHistory
from .entities.log import Log
from .enums.profile import Profile
from .enums.work_order_status import WorkOrderStatus


class UserEntityTests(unittest.TestCase):
    def test_is_admin_checks_administrator_profile(self):
        admin = User("Admin", "admin", Profile.ADMINISTRADOR)
        operator = User("Operator", "operator", Profile.OPERADOR)

        self.assertTrue(admin.is_admin())
        self.assertFalse(operator.is_admin())


class WorkOrderEntityTests(unittest.TestCase):
    @patch("hello.entities.work_order.connection.cursor")
    def test_create_inserts_order_and_returns_created_entity(self, cursor_factory):
        cursor = cursor_factory.return_value.__enter__.return_value
        cursor.lastrowid = 42

        work_order = WorkOrder.create(
            "Pump maintenance",
            "Inspect the main pump",
            WorkOrderStatus.IN_PROGRESS,
        )

        self.assertEqual(work_order.id, 42)
        self.assertEqual(work_order.status, WorkOrderStatus.IN_PROGRESS)
        cursor.execute.assert_called_once_with(
            ANY,
            ["Pump maintenance", "Inspect the main pump", "IN_PROGRESS"],
        )

    @patch("hello.entities.work_order.connection.cursor")
    def test_create_rejects_unknown_status_without_database_write(
        self, cursor_factory
    ):
        with self.assertRaises(ValueError):
            WorkOrder.create("Pump maintenance", "Inspect the main pump", "UNKNOWN")

        cursor_factory.assert_not_called()

    @patch("hello.entities.work_order.connection.cursor")
    def test_get_all_maps_database_rows_to_work_orders(self, cursor_factory):
        cursor = cursor_factory.return_value.__enter__.return_value
        cursor.fetchall.return_value = [
            (42, "Pump maintenance", "Inspect the main pump", "PENDING")
        ]

        work_orders = WorkOrder.get_all()

        self.assertEqual(len(work_orders), 1)
        self.assertEqual(work_orders[0].id, 42)
        self.assertEqual(work_orders[0].status, WorkOrderStatus.PENDING)


class WorkOrderHistoryEntityTests(unittest.TestCase):
    @patch("hello.entities.work_order_history.connection.cursor")
    def test_get_all_maps_database_rows_to_histories(self, cursor_factory):
        cursor = cursor_factory.return_value.__enter__.return_value
        cursor.fetchall.return_value = [
            ("2026-10-19", 7, "Created", 42)
        ]

        histories = WorkOrderHistory.get_all()

        self.assertEqual(len(histories), 1)
        self.assertEqual(histories[0].date, "2026-10-19")
        self.assertEqual(histories[0].user, 7)
        self.assertEqual(histories[0].action, "Created")
        self.assertEqual(histories[0].work_order, 42)
        cursor.execute.assert_called_once()


class LogEntityTests(unittest.TestCase):
    @patch("hello.entities.log.connection.cursor")
    def test_get_all_maps_database_rows_to_logs(self, cursor_factory):
        cursor = cursor_factory.return_value.__enter__.return_value
        cursor.fetchall.return_value = [
            ("2026-10-19", "Order created", 7, "work_order")
        ]

        logs = Log.get_all()

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].date, "2026-10-19")
        self.assertEqual(logs[0].description, "Order created")
        self.assertEqual(logs[0].user, 7)
        self.assertEqual(logs[0].module, "work_order")
        cursor.execute.assert_called_once()
