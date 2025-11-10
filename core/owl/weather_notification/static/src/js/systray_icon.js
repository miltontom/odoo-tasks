/** @odoo-module **/
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { Component, onWillStart } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

class SystrayIcon extends Component {
  setup() {
    super.setup(...arguments);
    onWillStart(() => {
      rpc("/current_weather").then((data) => {
        this.date = this.getDateString();
        this.temp = data.main.temp;
        this.city = data.name;
        this.description_main = data.weather[0].main;
        this.description = data.weather[0].description;
      });
    });
  }

  getDateString() {
    let date = new Date();
    let day = date.getDate();
    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];

    let month = months[date.getMonth()];
    let year = date.getFullYear();

    return `${day} ${month} ${year}`;
  }
}

SystrayIcon.template = "systray_icon";
SystrayIcon.components = { Dropdown, DropdownItem };
export const systrayItem = { Component: SystrayIcon };
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
