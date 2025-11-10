import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Popup } from "@pos_purchase_limit/js/popup";
import { AlertDialog, ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";


patch(PosStore.prototype, {
    async pay() {
        var purchaseLimitEnabled = this.config.customer_purchase_limit
        if (purchaseLimitEnabled) {
            var partner = this.get_order().partner_id;
            if (!partner) {
//                this.dialog.add(AlertDialog, {
//                    title: _t("Customer is required!"),
//                    body: _t("Please provide a customer"),
//                });
                this.dialog.add(Popup, {
                    title: _t("Customer is required!"),
                    body: _t("Please provide a customer"),
                });
                return;
            }

            var customerHasLimit = partner.activate_purchase_limit
            if (customerHasLimit) {
                var limit = partner.purchase_limit_amount;
                var total = this.get_order().getTotalDue();

                if (total > limit && limit != 0) {
                    this.dialog.add(AlertDialog, {
                        title: _t("Oops..."),
                        body: _t(`The purchase limit of amount ${limit} has been exceeded for the selected customer ${partner.name}.`),
                    });
                    return;
                }
            }
        }
        super.pay();
    }
});