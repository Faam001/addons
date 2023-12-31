# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import timedelta

from freezegun import freeze_time

from odoo import fields
from odoo.tests.common import Form, TransactionCase


@freeze_time("2023-02-01")
class TestFSMOrderBase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Order = self.env["fsm.order"]
        self.test_location = self.env.ref("fieldservice.test_location")


class TestFSMOrder(TestFSMOrderBase):
    def test_fsm_order(self):
        """Test creating new workorders, and test following functions,
        - _compute_duration() in hrs
        - _compute_request_late()
        - Set scheduled_date_start using request_early w/o time
        - scheduled_date_end = scheduled_date_start + duration (hrs)
        """
        # Create an Orders
        view_id = "fieldservice.fsm_order_form"
        hours_diff = 100
        with Form(self.Order, view=view_id) as f:
            f.location_id = self.test_location
            f.date_start = fields.Datetime.today()
            f.date_end = f.date_start + timedelta(hours=hours_diff)
            f.request_early = fields.Datetime.today()
        order = f.save()
        order._get_stage_color()
        self.assertEqual(order.custom_color, order.stage_id.custom_color)
        # Test _compute_duration
        self.assertEqual(order.duration, hours_diff)
        # Test _compute_request_late()
        priority_vs_late_days = {"0": 3, "1": 2, "2": 1, "3": 1 / 3}
        for priority, late_days in priority_vs_late_days.items():
            order.priority = priority
            order.request_late = False
            vals = {"request_early": fields.Datetime.today(), "priority": priority}
            vals = order._compute_request_late(vals)
            self.assertEqual(
                vals["request_late"],
                order.request_early + timedelta(days=late_days),
            )
        # Test scheduled_date_start is not automatically set
        self.assertEqual(
            order.scheduled_date_start,
            fields.Datetime.from_string("2023-02-01 00:00:00"),
        )
        # Test scheduled_date_end = scheduled_date_start + duration (hrs)
        # Set date start
        order.scheduled_date_start = fields.Datetime.now().replace(
            hour=0, minute=0, second=0
        )
        # Set duration
        duration = 10
        order.scheduled_duration = duration
        # Check date end
        self.assertEqual(
            order.scheduled_date_end, fields.Datetime.from_string("2023-02-01 10:00:00")
        )
        # Set new date end
        order.scheduled_date_end = order.scheduled_date_end.replace(
            hour=1, minute=1, second=0
        )
        # Check date start
        self.assertEqual(
            order.scheduled_date_start,
            fields.Datetime.from_string("2023-01-31 15:01:00"),
        )
