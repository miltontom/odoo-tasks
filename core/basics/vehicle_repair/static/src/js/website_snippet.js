import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from '@web/core/network/rpc';
import _ from './underscore'


publicWidget.registry.VehicleRepair = publicWidget.Widget.extend({
    selector: '.top-repairs',
    start: function () {
       var self = this
       rpc("/vehicle_repair/top_repairs", {}).then(function (result) {
           const obj = JSON.parse(result)
           var chunks = _.chunk(obj, 4) // split the array into multiple sub arrays
           chunks[0].is_active = true
           self.$target.empty().html(renderToElement('vehicle_repair.top_repairs_data', {chunks: chunks}))
       });
   },
});

export default publicWidget.registry.VehicleRepair;
