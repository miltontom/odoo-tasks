// not important

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { AlertDialog, ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        if (!this.currentOrder.get_partner()) {
            this.dialog.add(AlertDialog, {
                title: _t("Customer is required!"),
                body: _t("Please provide a customer"),
            });
            return;
        }

        var customerHasLimit = this.currentOrder.get_partner().activate_purchase_limit
        if (customerHasLimit && this.pos.config.customer_purchase_limit) {
            var limit = this.currentOrder.get_partner().purchase_limit_amount;
            var total = this.currentOrder.getTotalDue();

            if (total > limit && limit != 0) {
                this.dialog.add(AlertDialog, {
                    title: _t("Oops..."),
                    body: _t(`The purchase limit of amount ${limit} has been exceeded for the selected customer.`),
                });
                return;
            }
        }

        super.validateOrder(isForceValidate);
    }
});