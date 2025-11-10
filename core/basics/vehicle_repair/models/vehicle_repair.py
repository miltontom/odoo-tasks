# -*- coding: utf-8 -*-
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class VehicleRepair(models.Model):
    _name = "vehicle.repair"
    _description = "Vehicle Repair"
    _rec_name = "name"
    _order = "delivery_date desc"
    _inherit = "mail.thread"

    user_id = fields.Many2one(
        "res.users", string="Responsible User", default=lambda self: self.env.user
    )

    name = fields.Char(readonly=True, default="New", copy=False, tracking=True)
    date = fields.Date(default=date.today())
    name_id = fields.Many2one("res.partner", string="Customer", required=True)
    service_advisor_id = fields.Many2one("res.users", required=True)
    mobile = fields.Char(related="name_id.phone")
    vehicle_type_id = fields.Many2one("fleet.vehicle.model.category", required=True)
    vehicle_model_domain = fields.Binary(compute="_compute_vehicle_model_domain")
    vehicle_model_id = fields.Many2one(
        "fleet.vehicle.model",
        domain="[('category_id', '=', vehicle_type_id)]",
        required=True,
    )
    vehicle_model_id = fields.Many2one("fleet.vehicle.model", required=True)
    currency_id = fields.Many2one(
        "res.currency", "Currency", default=lambda self: self.env.company.currency_id
    )

    vehicle_number = fields.Char(copy=False)
    image = fields.Image()
    active = fields.Boolean(default=True)
    start_date = fields.Date(default=date.today())
    duration = fields.Integer(string="Duration (days)")
    delivery_date = fields.Date()
    service_type = fields.Selection(
        [("free", "Free"), ("paid", "Paid")], default="free"
    )
    estimated_amount = fields.Monetary(currency_field="currency_id")
    complaints = fields.Html()
    tag_ids = fields.Many2many("tag", string="Tags")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("ready_for_delivery", "Ready for Delivery"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    country = fields.Char(related="name_id.country_id.name")
    country_state = fields.Char(related="name_id.state_id.name")
    city = fields.Char(related="name_id.city")
    street = fields.Char(related="name_id.street")
    street2 = fields.Char(related="name_id.street2")
    zip = fields.Char(related="name_id.zip")

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    labor_cost_ids = fields.One2many("labor.cost", "vehicle_repair_id")
    consumed_part_ids = fields.One2many("consumed.part", "vehicle_repair_id")

    total_labor_cost_hours_spent = fields.Integer(related="labor_cost_ids.total_hours")
    total_labor_cost = fields.Float(
        related="labor_cost_ids.total", store=True
    )  # total of consumed parts
    total_consumed_parts = fields.Float(related="consumed_part_ids.total", store=True)

    estimated_delivery_date = fields.Date()

    invoice_id = fields.Many2one("account.move", string="Invoice")
    payment_status = fields.Selection(related="invoice_id.payment_state")

    cancelled_date = fields.Date(readonly=True)

    is_today = fields.Boolean(compute="_compute_is_today")
    is_tomorrow = fields.Boolean(compute="_compute_is_tomorrow")

    @api.depends("estimated_delivery_date", "state")
    def _compute_is_today(self):
        """
        Color records as red for estimated delivery date that is due today
        """
        for rec in self:
            rec.is_today = (
                rec.state == "in_progress"
                and rec.estimated_delivery_date == date.today()
            )

    @api.depends("estimated_delivery_date", "state")
    def _compute_is_tomorrow(self):
        """
        Color records as yellow for estimated delivery date that is due tomorrow
        """
        tomorrow = date.today() + timedelta(days=1)
        for rec in self:
            rec.is_tomorrow = (
                rec.state == "in_progress" and rec.estimated_delivery_date == tomorrow
            )

    @api.onchange("vehicle_type_id")
    def _onchange_vehicle_type(self):
        self.vehicle_model_id = None

    @api.depends("vehicle_type_id")
    def _compute_vehicle_model_domain(self):
        """
        Whenever vehicle type is empty vehicle model shows all categories
        """
        for rec in self:
            if rec.vehicle_type_id:
                rec.vehicle_model_domain = [
                    ("category_id", "in", [rec.vehicle_type_id.id])
                ]
            else:
                rec.vehicle_model_domain = []

    @api.depends("start_date", "duration")
    def _compute_delivery_date(self):
        """
        Calculates the duration for the repair in days
        """
        for record in self:
            # if not record.delivery_date:
            #     record.delivery_date = date.today()
            #     record.duration = (record.delivery_date - record.start_date).days
            # else:
            #     record.duration = (record.delivery_date - record.start_date).days
            record.delivery_date = record.start_date + relativedelta(
                days=record.duration
            )

    @api.model_create_multi
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].next_by_code("vehicle.repair") or "New"
            )
        return super().create(vals)

    def action_confirm(self):
        self.state = "in_progress"

    def change_customer_state(self):
        self.name_id.state = "service"

    def action_ready_for_delivery(self):
        self.state = "ready_for_delivery"
        template = self.env.ref("vehicle_repair.ready_for_delivery_template")
        template.send_mail(self.id, force_send=True)

    def action_done(self):
        self.state = "done"
        self.delivery_date = self.start_date + relativedelta(days=self.duration)

    def get_unpaid_invoices(self):
        unpaid_invoices = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("partner_id", "=", self.name_id.id),
                ("state", "in", ["draft", "posted"]),
                ("payment_state", "in", ["not_paid"]),
            ]
        )
        return unpaid_invoices

    def action_create_invoice(self):
        """
        Create invoice adding the consumed products and labor cost to the invoice line
        along with any unpaid invoices for a particular customer
        """
        for repair in self:
            if not repair.name_id:
                raise UserError("Please select a customer before creating an invoice.")

            if not repair.consumed_part_ids:
                raise UserError("Please add at least one consumed part.")

            invoice_lines = []

            for part in repair.consumed_part_ids:
                if not part.product_id:
                    continue

                new_line = (
                    0,
                    0,
                    {
                        "product_id": part.product_id.id,
                        "quantity": part.quantity,
                        "price_unit": part.unit_price,
                    },
                )

                invoice_lines.append(new_line)

            # add labor cost product
            invoice_lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": 54,  # id of labor cost product
                        "quantity": 1,
                        "price_unit": repair.total_labor_cost,
                        "name": "\n".join(
                            f"{r.employee.name} - {r.hours_spent}h"
                            for r in repair.labor_cost_ids
                        ),
                    },
                )
            )

            unpaid_invoices = repair.get_unpaid_invoices()

            if len(unpaid_invoices) > 0:
                invoice_lines.append(
                    (
                        0,
                        0,
                        {
                            "display_type": "line_section",
                            "name": "Unpaid invoice lines",
                        },
                    )
                )

            invoice = self.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": repair.name_id.id,
                    "invoice_origin": repair.name,
                    "invoice_line_ids": invoice_lines,
                    "invoice_date": fields.Date.today(),
                }
            )

            repair.invoice_id = invoice.id
            print(repair.invoice_id)

            # copy unpaid invoices of the customer to current invoice
            for inv in unpaid_invoices:
                for line in inv.invoice_line_ids:
                    line.copy({"move_id": invoice.id})

            for inv in unpaid_invoices:
                # inv.button_draft()
                inv.sudo().unlink()

            return {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "res_id": invoice.id,
                "view_mode": "form",
                "target": "current",
            }

    def action_view_invoices(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Invoice",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": self.invoice_id.id,
            "target": "current",
        }

    def action_cancel(self):
        for record in self:
            record.state = "cancelled"
            if not record.cancelled_date:
                record.cancelled_date = date.today()

    def archive_cancelled(self):
        """
        Archive cancelled records that's been over a month
        """
        to_archive = self.env["vehicle.repair"].search(
            [
                ("state", "=", "cancelled"),
            ]
        )

        current_date = date.today()
        for rec in to_archive:
            days_since_cancel = (current_date - rec.cancelled_date).days
            if days_since_cancel >= 30:
                rec.active = False
