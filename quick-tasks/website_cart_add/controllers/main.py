from odoo import http
from odoo.http import request


class Main(http.Controller):
    @http.route("/product_to_cart", type="http", auth="user", website=True)
    def product(self, **kwargs):
        options = {
            "products": request.env["product.product"].search([("sale_ok", "=", True)])
        }
        return request.render("website_cart_add.product_to_cart_page", options)

    @http.route("/add_to_cart", type="http", auth="user", website=True)
    def product_add(self, **kwargs):
        from pprint import pprint

        sale_order = request.website.sale_get_order(force_create=True)
        product_id = int(kwargs.get("product"))
        quantity = int(kwargs.get("quantity"))
        sale_order._cart_update(product_id=product_id, add_qty=quantity)
        return request.redirect("/shop/cart")
