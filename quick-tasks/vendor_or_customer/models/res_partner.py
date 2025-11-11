from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    state = fields.Selection(
        [("customer", "Customer"), ("vendor", "Vendor"), ("both", "Both")],
        compute="_compute_state",
    )

    def _compute_state(self):
        for rec in self:
            if rec.customer_rank > 0 and rec.supplier_rank > 0:
                rec.state = "both"
            elif rec.customer_rank > 0:
                rec.state = "customer"
            elif rec.supplier_rank > 0:
                rec.state = "vendor"
            else:
                rec.state = None
