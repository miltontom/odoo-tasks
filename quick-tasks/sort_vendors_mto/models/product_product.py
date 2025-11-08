from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_sellers(self, params=False):
        res = super()._prepare_sellers(params=params)
        return res.sorted(lambda s: (s.price, s.delay))
