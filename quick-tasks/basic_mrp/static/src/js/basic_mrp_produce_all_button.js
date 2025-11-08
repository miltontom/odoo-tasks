/** @odoo-module **/
console.log("loaded");
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {
  async updateButtons() {
    // call original method
    await super.updateButtons();

    // get current record data
    const record = this.model.root.data;
    const button = this.el.querySelector('button[name="action_produce"]');
    console.log(button);

    if (button) {
      // Disable button if quantity is 0
      console.log("button clicked");
      if (record.quantity === 0) {
        button.classList.add("disabled");
        button.setAttribute("disabled", "true");
      } else {
        button.classList.remove("disabled");
        button.removeAttribute("disabled");
      }
    }
  },
});
