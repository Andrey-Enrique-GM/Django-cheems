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
        self.assertEqual(work_orders[0].status, WorkOrderStatus.PENDING)

    @patch("hello.entities.work_order.connection.cursor")
    def test_update_status_changes_only_status(self, cursor_factory):
        cursor = cursor_factory.return_value.__enter__.return_value

        WorkOrder.update_status(42, WorkOrderStatus.COMPLETED)

        cursor.execute.assert_called_once_with(
            "UPDATE work_order SET status = %s WHERE id = %s",
            [WorkOrderStatus.COMPLETED.value, 42],
        )


class CreateWorkOrderViewTests(unittest.TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    @patch("hello.views.WorkOrder.create")
    @patch("hello.views.WorkOrderHistory.create")
    @patch("hello.views.Log.create")
    @patch("hello.views.get_current_user")
    def test_create_always_starts_pending_even_if_request_includes_another_status(
        self, get_current_user, create_log, create_history, create_work_order
    ):
        get_current_user.return_value = User(
            "Admin", "admin", Profile.ADMINISTRADOR, id=7
        )
        create_work_order.return_value = WorkOrder(
            "Pump maintenance", "Inspect the main pump", WorkOrderStatus.PENDING, id=42
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
        )
        create_history.assert_called_once_with(
            id_user=7, action=WorkOrderStatus.PENDING.value, id_work_order=42
        )

    @patch("hello.views.WorkOrder.create")
    @patch("hello.views.WorkOrderHistory.create")
    @patch("hello.views.Log.create")
    @patch("hello.views.get_current_user")
    def test_create_does_not_require_a_status_in_the_request(
        self, get_current_user, create_log, create_history, create_work_order
    ):
        get_current_user.return_value = User(
            "Admin", "admin", Profile.ADMINISTRADOR, id=7
        )
        create_work_order.return_value = WorkOrder(
            "Pump maintenance", "Inspect", WorkOrderStatus.PENDING, id=42
        )
        request = self.request_factory.post(
            "/create-work-order/",
            {"title": "Pump maintenance", "description": "Inspect"},
        )

        response = views.create_work_order(request)

        self.assertEqual(response.status_code, 302)
        create_work_order.assert_called_once_with(
            title="Pump maintenance", description="Inspect"
        )


class UpdateWorkOrderStatusViewTests(unittest.TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    @patch("hello.views.WorkOrder.update_status")
    @patch("hello.views.WorkOrderHistory.create")
    @patch("hello.views.Log.create")
    @patch("hello.views.get_current_user")
    def test_status_update_changes_only_status(
        self, get_current_user, create_log, create_history, update_status
    ):
        get_current_user.return_value = User(
            "Admin", "admin", Profile.ADMINISTRADOR, id=7
        )
        request = self.request_factory.post(
            "/update-work-order-status/42/",
            {
                "status": str(WorkOrderStatus.COMPLETED.value),
                "title": "Should be ignored",
                "description": "Should also be ignored",
            },
        )

        response = views.update_work_order_status(request, order_id=42)

        self.assertEqual(response.status_code, 302)
        update_status.assert_called_once_with(
            order_id=42, status=WorkOrderStatus.COMPLETED
        )
        create_history.assert_called_once_with(
            id_user=7,
            action=WorkOrderStatus.COMPLETED.value,
            id_work_order=42,
        )

    @patch("hello.views.WorkOrder.update_status")
    @patch("hello.views.get_current_user")
    def test_status_update_rejects_invalid_state(
        self, get_current_user, update_status
    ):
        get_current_user.return_value = User(
            "Admin", "admin", Profile.ADMINISTRADOR, id=7
        )
        request = self.request_factory.post(
            "/update-work-order-status/42/", {"status": "invalid"}
        )

        response = views.update_work_order_status(request, order_id=42)

        self.assertEqual(response.status_code, 400)
        update_status.assert_not_called()


class WorkOrderHistoryEntityTests(unittest.TestCase):
    @patch("hello.entities.work_order_history.connection.cursor")
    def test_get_all_maps_database_rows_to_histories(self, cursor_factory):
        cursor = cursor_factory.return_value.__enter__.return_value
        cursor.fetchall.return_value = [
            (1, "2026-10-19", 7, "Created", 42)
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
            (3, "2026-10-19", "Order created", 7, 2)
        ]

        logs = Log.get_all()

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].date, "2026-10-19")
        self.assertEqual(logs[0].description, "Order created")
        self.assertEqual(logs[0].id_user, 7)
        self.assertEqual(logs[0].module, 2)
        cursor.execute.assert_called_once()
        self.assertIn("id_user", cursor.execute.call_args.args[0])
