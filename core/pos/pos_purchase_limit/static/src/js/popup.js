/** @odoo-module */
import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";

export class Popup extends Component {
    static template = "pos_custom_popup.popup";
    static components = { Dialog };
    static props = {
        close: Function,
        body: { type: String, optional: true },
        title: {
            validate: (m) => {
                return (
                    typeof m === "string" ||
                    (typeof m === "object" && typeof m.toString === "function")
                );
            },
            optional: true,
        },
    }
    async confirm() {
        this.props.close();
    }
}
