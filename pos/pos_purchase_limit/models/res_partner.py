from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    activate_purchase_limit = fields.Boolean(string="Activate Purchase Limit")
    purchase_limit_amount = fields.Float()
    customer_purchase_limit = fields.Boolean(compute="_compute_customer_purchase_limit")

    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ["activate_purchase_limit", "purchase_limit_amount"]
        return result

    def _compute_customer_purchase_limit(self):
        pc_sudo = self.env["pos.config"].sudo()
        param = pc_sudo.search([])
        print(any([r.customer_purchase_limit for r in param]))
        self.customer_purchase_limit = any([r.customer_purchase_limit for r in param])