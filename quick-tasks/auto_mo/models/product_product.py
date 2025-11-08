import logging

from odoo import Command
from odoo import fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger("__name__")


class ProductProduct(models.Model):
    _inherit = "product.product"

    def is_manuf_faster(self):
        if not self.variant_seller_ids:
            raise ValidationError("Please provide a vendor for the product.")

        vendor_id = self.variant_seller_ids[:1]
        bom_id = self.bom_ids[:1]

        return bom_id.produce_delay < vendor_id.delay

    def two_routes_enabled(self, route_a, route_b):
        route_ids = self.route_ids.ids

        return route_a.id in route_ids and route_b.id in route_ids

    def create_purchase_order(self, vals=None):
        lines = []
        sale_order = self.env["sale.order"].browse(vals.get("sale_order_id"))
        for line in sale_order.order_line:
            lines.append(
                Command.create(
                    {
                        "product_id": line.product_id.id,
                        "product_qty": line.product_uom_qty,
                        "price_unit": line.price_unit,
                        "price_subtotal": line.price_subtotal,
                    }
                )
            )

        res_id = self.env["purchase.order"].create(
            {"partner_id": vals.get("partner_id"), "order_line": lines}
        )

        return res_id

    def create_order(self, vals=None):
        manuf_route_id = self.env.ref("mrp.route_warehouse0_manufacture")
        buy_route_id = self.env.ref("purchase_stock.route_warehouse0_buy")

        if self.qty_available > self.threshold:
            return

        if not self.two_routes_enabled(manuf_route_id, buy_route_id):
            return

        if not self.is_manuf_faster():
            res_id = self.create_purchase_order(vals)
            return (False, res_id)

        res_id = self.env["mrp.production"].create({"product_id": self.id})

        return (True, res_id)
