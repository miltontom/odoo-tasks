from odoo import fields, models, api


class LaborCost(models.Model):
    _name = "labor.cost"
    _description = "Labor cost for vehicle repairs"

    employee = fields.Many2one("hr.employee")
    currency_id = fields.Many2one(
        "res.currency", "Currency", default=lambda self: self.env.company.currency_id
    )
    hourly_cost = fields.Monetary(
        related="employee.hourly_cost", currency_field="currency_id"
    )
    hours_spent = fields.Integer()
    subtotal = fields.Float(compute="_compute_subtotal", store=True)
    total = fields.Float(compute="_compute_total")
    total_hours = fields.Integer(compute="_compute_total_hours")

    vehicle_repair_id = fields.Many2one("vehicle.repair")

    @api.depends("hours_spent", "hourly_cost")
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.hours_spent * rec.hourly_cost

    @api.depends("subtotal")
    def _compute_total(self):
        for rec in self:
            rec.total = sum([rec.subtotal for rec in self])

    @api.depends("hours_spent")
    def _compute_total_hours(self):
        for rec in self:
            rec.total_hours = sum([rec.hours_spent for rec in self])
