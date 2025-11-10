/** @odoo-module */

import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  onWillUpdateProps,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class ChartRenderer extends Component {
  setup() {
    this.chartRef = useRef("chart");
    this.chart = null;

    onWillStart(async () => {
      await loadJS(
        "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"
      );
    });

    onMounted(() => {
      this.renderChart(this.props.data);
    });

    onWillUpdateProps((nextProps) => {
      if (this.chart) {
        this.updateChart(nextProps.data);
      } else {
        this.renderChart(nextProps.data);
      }
    });
  }

  generateColors(count) {
    return Array.from({ length: count }, () => {
      const r = Math.floor(Math.random() * 256);
      const g = Math.floor(Math.random() * 256);
      const b = Math.floor(Math.random() * 256);
      return `rgb(${r}, ${g}, ${b})`;
    });
  }

  renderChart(data) {
    this.chart = new Chart(this.chartRef.el, {
      type: this.props.type,
      data: {
        labels: data.map((row) => row.label),
        datasets: [
          {
            label: "Count",
            data: data.map((row) => row.count),
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  updateChart(newData) {
    let colors = this.generateColors(newData.length);
    this.chart.data.labels = newData.map((row) => row.label);
    this.chart.data.datasets[0].data = newData.map((row) => row.count);
    this.chart.data.datasets[0].backgroundColor = colors;
    this.chart.update();
  }
}

ChartRenderer.template = "crm_dashboard.ChartRenderer";
