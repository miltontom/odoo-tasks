import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(Orderline.prototype, {
    setup() {
        this.pos = usePos();
    },
    onClickDelete() {
        var order = this.pos.get_order();
        var selectedLine = order.get_selected_orderline();
        order.removeOrderline(selectedLine)
    }
});