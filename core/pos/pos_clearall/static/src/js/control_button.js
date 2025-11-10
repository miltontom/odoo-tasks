import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";


patch(ControlButtons.prototype, {
    onClickClearAll() {
        var order = this.pos.get_order();
        var order_lines = order.get_orderlines();

        order_lines.filter(line => line.get_product()).forEach(line => order.removeOrderline(line));
    }
});