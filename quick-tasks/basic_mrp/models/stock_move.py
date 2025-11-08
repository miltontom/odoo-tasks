from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_procurement_values(self):
        res = super()._prepare_procurement_values()
        from pprint import pprint

        pprint(res)
        bom_line = self.env['mrp.bom'].browse(res.get('bom_line_id'))
        print(bom_line.product_id.name)
        return res
