from odoo import api, fields, models
from pprint import pprint


class SaleOrder(models.Model):
    _inherit = "sale.order"

    currency_id = fields.Many2one("res.currency")
    salesperson_commission = fields.Monetary(
        currency_field="currency_id", compute="_compute_salesperson_commission"
    )

    @api.depends("order_line")
    def _compute_salesperson_commission(self):
        sales_person = self.env["crm.team.member"].search(
            [("user_id", "=", self.user_id.id)]
        )
        commission = sales_person.commission_id

        if commission.commission_type == "product":
            commission_products = set(
                commission.commission_product_ids.mapped("product_id").ids
            )
            order_line_products = set(self.order_line.mapped("product_id").ids)

            to_commission_products = commission_products.intersection(
                order_line_products
            )

            products = commission.commission_product_ids.filtered(
                lambda x: x.product_id.id in to_commission_products
            ).sorted(key=lambda r: r.product_id.id)

            order_line_prods = self.order_line.filtered(
                lambda x: x.product_id.id in to_commission_products
            ).sorted(key=lambda r: r.product_id.id)

            commission = 0
            for order_line, comm_prod_line in zip(order_line_prods, products):

                if order_line.price_subtotal >= comm_prod_line.max_amount:
                    commission += order_line.price_subtotal * (
                        comm_prod_line.percent_rate / 100
                    )
            self.salesperson_commission = commission
        elif commission.commission_type == "revenue":
            if commission.commission_revenue_type == "straight":
                self.salesperson_commission = self.calculate_revenue_straight(
                    commission
                )
            elif commission.commission_revenue_type == "graduated":
                self.salesperson_commission = self.calculate_revenue_graduated(
                    sales_person, commission
                )
        else:
            self.salesperson_commission = 0

    def calculate_revenue_straight(self, commission):
        return self.amount_total * (commission.percent_rate / 100)

    def calculate_revenue_graduated(self, sales_person, commission):
        if sales_person.first_target_achieved:
            return self.amount_total * (commission.percent_rate_second / 100)

        return self.amount_total * (commission.percent_rate_first / 100)

    def _action_confirm(self):
        sales_person = self.env["crm.team.member"].search(
            [("user_id", "=", self.user_id.id)]
        )

        if not sales_person.first_target_achieved:
            sales_person.first_target_achieved = True
