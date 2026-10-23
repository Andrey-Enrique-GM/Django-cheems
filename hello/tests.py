import unittest
from unittest.mock import ANY, patch
from django.test import RequestFactory

from . import views
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
            "2",
        )

        self.assertEqual(work_order.id, 42)
        self.assertEqual(work_order.status, WorkOrderStatus.IN_PROGRESS)
        cursor.execute.assert_called_once_with(
            ANY,
            ["Pump maintenance", "Inspect the main pump", 2],
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
            (42, "Pump maintenance", "Inspect the main pump", 1)
        ]

        work_orders = WorkOrder.get_all()

        self.assertEqual(len(work_orders), 1)
        self.assertEqual(work_orders[0].id, 42)
        self.assertEqual(work_orders[0].status, WorkOrderStatus.PENDIENTE)


class CreateWorkOrderViewTests(unittest.TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    @patch("hello.views.WorkOrder.create")
    @patch("hello.views.get_current_user")
    def test_create_passes_numeric_form_status_to_entity(
        self, get_current_user, create_work_order
    ):
        get_current_user.return_value = User(
            "Admin", "admin", Profile.ADMINISTRADOR
        )
        request = self.request_factory.post(
            "/create-work-order/",
            {
                "title": "Pump maintenance",
                "description": "Inspect the main pump",
                "status": "2",
            },
        )

        response = views.create_work_order(request)

        self.assertEqual(response.status_code, 302)
        create_work_order.assert_called_once_with(
            title="Pump maintenance",
            description="Inspect the main pump",
            status=WorkOrderStatus.IN_PROGRESS,
        )

    @patch("hello.views.WorkOrder.create")
    @patch("hello.views.get_current_user")
    def test_create_rejects_non_numeric_status(
        self, get_current_user, create_work_order
    ):
        get_current_user.return_value = User(
            "Admin", "admin", Profile.ADMINISTRADOR
        )
        request = self.request_factory.post(
            "/create-work-order/",
            {"title": "Pump maintenance", "description": "Inspect", "status": "PENDIENTE"},
        )

        response = views.create_work_order(request)

        self.assertEqual(response.status_code, 400)
        create_work_order.assert_not_called()


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
        self.assertEqual(histories[0].id_user, 7)
        self.assertEqual(histories[0].action, "Created")
        self.assertEqual(histories[0].id_work_order, 42)
        cursor.execute.assert_called_once()
        self.assertIn("id_user", cursor.execute.call_args.args[0])


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
        self.assertEqual(logs[0].id_user, 7)
        self.assertEqual(logs[0].module, "work_order")
        cursor.execute.assert_called_once()
        self.assertIn("id_user", cursor.execute.call_args.args[0])
