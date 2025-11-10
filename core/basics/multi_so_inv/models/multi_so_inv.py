from odoo import fields, models, api, Command


class MultiSOInv(models.Model):
    _name = "multi.so.inv"
    _description = "Invoice multiple sale orders"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    sale_order_ids = fields.Many2many("sale.order", string="Sale Orders", domain="[('partner_id', '=', partner_id), ('state', '=', 'sale'), ('invoice_status', '=', 'to invoice')]")  # confirmed sales orders that are to be invoiced
    order_line_ids = fields.One2many("so.order.line", "multi_so_inv_id")
    active = fields.Boolean(default=True)
    total_amount = fields.Float(related="order_line_ids.total_amount")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    @api.onchange('sale_order_ids')
    def _onchange_sale_order_ids(self):
        lines = []
        for so in self.sale_order_ids:
            for line in so.order_line:
                lines.append((0, 0, {
                    'product_id': line.product_id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal
                }))
        self.order_line_ids = [Command.clear()] + lines
