from odoo import api, fields, models


class PaymentLine(models.TransientModel):
    _name = "payment.line"

    sale_order_id = fields.Many2one("sale.order")
    make_pos_order_id = fields.Many2one("make.pos.order.wizard")
    shop_id = fields.Many2one(related="make_pos_order_id.shop_id")
    payment_method_id = fields.Many2one(
        "pos.payment.method", domain="[('config_ids', 'in', [shop_id])]"
    )
    amount_paid = fields.Float()
