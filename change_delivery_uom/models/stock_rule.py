from odoo import fields, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_dest_id,
        name,
        origin,
        company_id,
        values,
    ):
        res = super()._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_dest_id,
            name,
            origin,
            company_id,
            values,
        )

        sale_order_line = self.env["sale.order.line"].browse(values.get("sale_line_id"))
        change_delivery_uom_enabled = sale_order_line.order_id.change_delivery_uom

        if change_delivery_uom_enabled:
            delivery_uom = sale_order_line.product_id.delivery_uom
            uom = sale_order_line.product_uom
            qty = sale_order_line.product_uom_qty

            converted_quantity = uom._compute_quantity(qty, delivery_uom)

            res.update(
                {"product_uom_qty": converted_quantity, "product_uom": delivery_uom.id}
            )

        return res
