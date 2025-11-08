from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError


class BasicMrp(models.Model):
    _name = "basic.mrp"

    name = fields.Char(readonly=True, default="New", copy=False, tracking=True)
    product_id = fields.Many2one("product.product", required=True)
    quantity = fields.Integer(default=1)
    bom_id = fields.Many2one("basic.bom")
    component_ids = fields.One2many(
        "basic.mrp.component",
        "basic_mrp_id",
        compute="_compute_component_ids",
        readonly=False,
        store=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("wait_for_qtys", "Waiting for Quantities"),
            ("done", "Done"),
        ],
        default="draft",
    )
    purchase_order_ids = fields.One2many("purchase.order", "basic_mrp_id")
    purchase_order_count = fields.Integer(compute="_compute_purchase_order_count")

    @api.depends("purchase_order_ids")
    def _compute_purchase_order_count(self):
        self.purchase_order_count = len(self.purchase_order_ids)

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.bom_id = self.product_id.basic_bom_ids[:1]

    @api.onchange("quantity")
    def _onchange_quantity(self):
        def change_quantity(s):
            corresponding_line = self.bom_id.component_ids.filtered(
                lambda x: x.product_id == s.product_id
            )
            s.quantity = corresponding_line.quantity * self.quantity

        self.component_ids.mapped(change_quantity)

    @api.onchange("bom_id")
    def _onchange_bom_id(self):
        self.quantity = self.bom_id.quantity

    @api.depends("bom_id")
    def _compute_component_ids(self):
        lines = [
            Command.create(
                {"product_id": line.product_id.id, "quantity": line.quantity}
            )
            for line in self.bom_id.component_ids
        ]
        self.component_ids = [Command.clear()] + lines

    def can_proceed_to_manufacture(self):
        for line in self.component_ids:
            on_hand = line.product_id.qty_available
            if on_hand < line.quantity:
                return False
        return True

    def action_confirm(self):
        if not self.product_id.basic_bom_ids:
            raise ValidationError("There is no BoM configured for the product")

        if self.can_proceed_to_manufacture():
            self.action_produce()
            self.write({"state": "done"})
        else:
            for line in self.component_ids:
                on_hand = line.product_id.qty_available
                if on_hand <= line.quantity:
                    order_line = [
                        Command.create(
                            {
                                "product_id": line.product_id.id,
                                "product_qty": line.quantity - on_hand,
                                "price_unit": line.product_id.standard_price,
                            }
                        )
                    ]
                    po = self.env["purchase.order"].create(
                        {
                            "partner_id": line.product_id.seller_ids[:1].id,
                            "order_line": order_line,
                        }
                    )
                    self.purchase_order_ids = [Command.link(po.id)]
            self.write({"state": "wait_for_qtys"})

    def action_produce(self):
        # update onhand quantity of product and components
        # product +
        # components -
        if not self.can_proceed_to_manufacture():
            raise ValidationError("There is not enough quantities to manufacture.")

        quant = self.env["stock.quant"]
        location = self.env.ref("stock.stock_location_stock")

        # increase product quantity
        quant._update_available_quantity(self.product_id, location, self.quantity)

        # decrease components quantity
        for line in self.component_ids:
            quant._update_available_quantity(line.product_id, location, -line.quantity)

        self.write({"state": "done"})

    def action_view_created_purchase_orders(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_type": "list",
            "view_mode": "list,form",
            "domain": [["basic_mrp_id", "=", self.id]],
            "target": "current",
        }

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get("name", "New") == "New":
                val["name"] = self.env["ir.sequence"].next_by_code("basic.mrp") or "New"
            return super().create(vals)
