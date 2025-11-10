from odoo import fields, models, api


class ConsumedPart(models.Model):
    _name = "consumed.part"
    _description = "Consumed parts for a vehicle repair"

    quantity = fields.Integer()
    product_id = fields.Many2one(
        "product.product", domain="[('type', 'in', ['consu', 'service'])]"
    )
    subtotal = fields.Float(compute="_compute_subtotal")
    total = fields.Float(compute="_compute_total")
    unit_price = fields.Float(compute="_compute_unit_price")
    vehicle_repair_id = fields.Many2one("vehicle.repair")

    @api.onchange("product_id")
    def set_quantity(self):
        self.quantity = 1

    @api.depends("unit_price", "quantity")
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.unit_price * rec.quantity

    @api.depends("product_id.list_price")
    def _compute_unit_price(self):
        for rec in self:
            rec.unit_price = rec.product_id.list_price

    @api.depends("subtotal")
    def _compute_total(self):
        for rec in self:
            rec.total = sum([rec.subtotal for rec in self])
