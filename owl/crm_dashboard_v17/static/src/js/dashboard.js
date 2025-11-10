/** @odoo-module */
import { Component, onWillStart, useRef, onMounted, useState } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Card } from "./card/card";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
const { DateTime, Interval } = luxon;
import { session } from "@web/session";

class CRMDashboard extends Component {
  setup() {
    this.state = useState({
      leads: {
        value: 0,
      },
      opportunities: {
        value: 0,
      },
      expectedRevenue: {
        value: 0,
      },
      revenue: {
        value: 0,
      },
      wonLostOpp: {
        value: 0,
      },
      period: 0,
      charts: {
        leadsByMedium: [],
        activities: [],
        lostLeadsOpps: [],
        leadsByMonth: [],
        leadsByCampaign: [],
      },
    });

    this.orm = useService("orm");
    this.actionService = useService("action");
    this.user_id = session.uid;

    onWillStart(async () => {
      this.getDates();
      await this.getLeads();
      await this.getOpportunities();
      await this.getExpectedRevenue();
      await this.getRevenue();
      await this.getWonLostOpp();
      await this.getLeadsByMedium();
      await this.getActivities();
      await this.getLostLeadOpps();
      await this.getLeadsByMonth();
      await this.getLeadsByCampaign();
    });
  }

  async onChangePeriod() {
    this.getDates();
    await this.getLeads();
    await this.getOpportunities();
    await this.getExpectedRevenue();
    await this.getRevenue();
    await this.getWonLostOpp();
    await this.getLeadsByMedium();
    await this.getActivities();
    await this.getLostLeadOpps();
    await this.getLeadsByMonth();
    await this.getLeadsByCampaign();
  }

  /* Cards */

  getQuarterlyDates(quarter) {
    let yearQuarter = [];
    let now = DateTime.now();
    let startDate = DateTime.local(now.year, 1, 1);
    let start = startDate;
    let end = null;
    for (let i = 1; i <= 4; i++) {
      let end = start.plus({ month: 3 });
      yearQuarter.push({
        start: start,
        end: end,
      });
      start = end;
    }

    return quarter ? yearQuarter[quarter - 1] : yearQuarter;
  }

  async getCompanyCurrency() {
    const result = await jsonrpc("/get/company_currency", {});
    return result;
  }

  getDates() {
    let now = DateTime.now();
    let days = this.state.period;
    if (days == 365) {
      let quarterlyDates = this.getQuarterlyDates();
      let start = quarterlyDates[0].start;
      let end = quarterlyDates[3].end;
      this.state.startDate = start;
      this.state.endDate = end;
    } else if (days == 90) {
      let { start, end } = this.getQuarterlyDates(now.quarter);
      this.state.startDate = start;
      this.state.endDate = end;
    } else if (days == 30) {
      let start = DateTime.local(now.year, now.month, 1);
      let end = start.plus({ month: 1 });
      this.state.startDate = start;
      this.state.endDate = end;
    } else if (days == 7) {
      const WEEKDAYS = 7;
      let reverseWeekdays = { 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1 };
      let start = WEEKDAYS - reverseWeekdays[now.weekday];
      let end = WEEKDAYS - now.weekday;
      this.state.startDate = now.minus({ day: start });
      this.state.endDate = now.plus({ day: end });
    } else {
    }
  }

  /* Cards */

  async getLeads() {
    let domain = [
      ["type", "=", "lead"],
      ["user_id", "=", this.user_id],
    ];
    if (this.state.period != 0) {
      domain.push(["create_date", ">=", this.state.startDate]);
      domain.push(["create_date", "<", this.state.endDate]);
    }

    const data = await this.orm.searchCount("crm.lead", domain);
    this.state.leads.value = data;
  }

  async getOpportunities() {
    let domain = [
      ["user_id", "=", this.user_id],
      ["type", "=", "opportunity"],
    ];

    if (this.state.period != 0) {
      domain.push(["date_open", ">=", this.state.startDate]);
      domain.push(["date_open", "<", this.state.endDate]);
    }

    const data = await this.orm.searchCount("crm.lead", domain);
    this.state.opportunities.value = data;
  }

  async getExpectedRevenue() {
    let domain = [
      ["type", "=", "opportunity"],
      ["user_id", "=", this.user_id],
    ];

    if (this.state.period != 0) {
      domain.push(["date_open", ">=", this.state.startDate]);
      domain.push(["date_open", "<", this.state.endDate]);
    }
    const data = await this.orm.searchRead("crm.lead", domain, [
      "expected_revenue",
    ]);
    let total = 0;
    data.forEach((element) => {
      total += element.expected_revenue;
    });
    let currencySymbol = await this.getCompanyCurrency();
    this.state.expectedRevenue.value = `${JSON.parse(currencySymbol)}${(
      total / 1000
    ).toFixed(2)}K`;
  }

  async getRevenue() {
    let domain = [
      ["user_id", "=", this.user_id],
      ["move_type", "=", "out_invoice"],
    ];

    if (this.state.period != 0) {
      domain.push(["invoice_date", ">=", this.state.startDate]);
      domain.push(["invoice_date", "<", this.state.endDate]);
    }
    const data = await this.orm.searchRead("account.move", domain, [
      "amount_total",
    ]);
    let total = 0;
    data.forEach((el) => {
      total += el.amount_total;
    });
    let currencySymbol = await this.getCompanyCurrency();
    this.state.revenue.value = `${JSON.parse(currencySymbol)}${(
      total / 1000
    ).toFixed(2)}K`;
  }

  async getWonLostOpp() {
    let domain = [
      ["stage_id.is_won", "=", "true"],
      ["user_id", "=", this.user_id],
      ["type", "=", "opportunity"],
    ];
    if (this.state.period != 0) {
      domain.push(["date_closed", ">=", this.state.startDate]);
      domain.push(["date_closed", "<", this.state.endDate]);
    }
    const won = await this.orm.searchCount("crm.lead", domain);

    domain = [
      ["probability", "=", 0],
      ["active", "=", false],
      ["user_id", "=", this.user_id],
      ["type", "=", "opportunity"],
    ];

    if (this.state.period != 0) {
      domain.push(["date_closed", ">=", this.state.startDate]);
      domain.push(["date_closed", "<", this.state.endDate]);
    }

    const lost = await this.orm.searchCount("crm.lead", domain);
    this.state.wonLostOpp.value = ` ${won}/${lost} `;
  }

  viewLeads() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Leads",
      res_model: "crm.lead",
      domain: [
        ["type", "=", "lead"],
        ["user_id", "=", this.user_id],
      ],
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  async viewOpportunities() {
    /* for a specific view */
    let view = await this.orm.searchRead(
      "ir.model.data",
      [["name", "=", "crm_case_tree_view_oppor"]],
      ["res_id"]
    );

    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Opportunities",
      res_model: "crm.lead",
      domain: [
        ["type", "=", "opportunity"],
        ["user_id", "=", this.user_id],
      ],
      views: [
        /* if there are multiple views, the view with a lower sequence is taken, 
        the variable 'view' can be passed as the first element to the list.
        conditionally add the view if it exists else keep it as false */
        [view.length > 0 ? view[0].res_id : false, "list"],
        [false, "form"],
      ],
    });
  }

  viewExpectedRevenue() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Expected Revenue",
      res_model: "crm.lead",
      domain: [["user_id", "=", this.user_id]],
      views: [[false, "pivot"]],
    });
  }

  viewRevenue() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Invoices",
      res_model: "account.move",
      domain: [
        ["move_type", "=", "out_invoice"],
        ["user_id", "=", this.user_id],
      ],
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  viewWinLossOpp() {
    return;
  }

  /* Charts */

  async getLeadsByMedium() {
    let domain = [
      ["user_id", "=", this.user_id],
      ["type", "=", "lead"],
    ];

    if (this.state.period != 0) {
      domain.push(["create_date", ">=", this.state.startDate]);
      domain.push(["create_date", "<", this.state.endDate]);
    }
    const data = await this.orm.searchRead("crm.lead", domain, ["medium_id"]);

    let dataset = {};
    data.forEach((r) => {
      let medium = r.medium_id;
      if (medium && !dataset[medium[1]]) {
        dataset[medium[1]] = 0;
      }
      if (medium) {
        dataset[medium[1]] += 1;
      }
    });

    let new_dataset = [];
    for (let o in dataset) {
      new_dataset.push({ label: o, count: dataset[o] });
    }
    this.state.charts.leadsByMedium = new_dataset;
  }

  async getActivities() {
    let domain = [
      ["user_id", "=", this.user_id],
      ["res_model", "=", "crm.lead"],
    ];

    if (this.state.period != 0) {
      domain.push(["create_date", ">=", this.state.startDate]);
      domain.push(["create_date", "<", this.state.endDate]);
    }

    const data = await this.orm.searchRead("mail.activity", domain);
    let dataset = {};
    data.forEach((r) => {
      let activity = r.activity_type_id;
      if (activity && !dataset[activity[1]]) {
        dataset[activity[1]] = 0;
      }
      if (activity) {
        dataset[activity[1]] += 1;
      }
    });

    let new_dataset = [];
    for (let o in dataset) {
      new_dataset.push({ label: o, count: dataset[o] });
    }
    this.state.charts.activities = new_dataset;
  }

  monthFromInt(m) {
    if (!(m >= 1 && m <= 12)) {
      return;
    }
    const MONTHS_INT = {
      1: "Jan",
      2: "Feb",
      3: "Mar",
      4: "Apr",
      5: "May",
      6: "Jun",
      7: "Jul",
      8: "Aug",
      9: "Sep",
      10: "Oct",
      11: "Nov",
      12: "Dec",
    };
    return MONTHS_INT[m];
  }

  async getLostLeadOpps() {
    let monthlyData = {
      Jan: 0,
      Feb: 0,
      Mar: 0,
      Apr: 0,
      May: 0,
      Jun: 0,
      Jul: 0,
      Aug: 0,
      Sep: 0,
      Oct: 0,
      Nov: 0,
      Dec: 0,
    };

    let now = DateTime.now();
    let startDate = DateTime.local(now.year, 1, 1);
    let endDate;

    for (let i = 1; i <= 12; i++) {
      endDate = startDate.plus({ month: 1 });

      const data = await this.orm.searchCount("crm.lead", [
        ["type", "in", ["opportunity", "lead"]],
        ["user_id", "=", this.user_id],
        ["active", "=", false],
        ["probability", "=", 0],
        ["date_closed", ">=", startDate],
        ["date_closed", "<", endDate],
      ]);

      startDate = endDate;
      monthlyData[this.monthFromInt(i)] = data;
    }

    let newData = [];
    for (let m in monthlyData) {
      newData.push({ label: m, count: monthlyData[m] });
    }

    this.state.charts.lostLeadsOpps = newData;
  }

  async getLeadsByMonth() {
    let monthlyData = {
      Jan: 0,
      Feb: 0,
      Mar: 0,
      Apr: 0,
      May: 0,
      Jun: 0,
      Jul: 0,
      Aug: 0,
      Sep: 0,
      Oct: 0,
      Nov: 0,
      Dec: 0,
    };

    let now = DateTime.now();
    let startDate = DateTime.local(now.year, 1, 1);
    let endDate;

    for (let i = 1; i <= 12; i++) {
      endDate = startDate.plus({ month: 1 });

      const data = await this.orm.searchCount("crm.lead", [
        ["type", "=", "lead"],
        ["user_id", "=", this.user_id],
        ["create_date", ">=", startDate],
        ["create_date", "<", endDate],
      ]);

      startDate = endDate;
      monthlyData[this.monthFromInt(i)] = data;
    }

    let newData = [];
    for (let m in monthlyData) {
      newData.push({ label: m, count: monthlyData[m] });
    }

    this.state.charts.leadsByMonth = newData;
  }

  async getLeadsByCampaign() {
    let domain = [
      ["user_id", "=", this.user_id],
      ["type", "=", "lead"],
    ];

    if (this.state.period != 0) {
      domain.push(["create_date", ">=", this.state.startDate]);
      domain.push(["create_date", "<", this.state.endDate]);
    }
    const data = await this.orm.searchRead("crm.lead", domain, ["campaign_id"]);

    let dataset = {};
    data.forEach((r) => {
      let campaign = r.campaign_id;
      if (campaign && !dataset[campaign[1]]) {
        dataset[campaign[1]] = 0;
      }
      if (campaign) {
        dataset[campaign[1]] += 1;
      }
    });

    let new_dataset = [];
    for (let o in dataset) {
      new_dataset.push({ label: o, count: dataset[o] });
    }
    this.state.charts.leadsByCampaign = new_dataset;
  }

  viewLeadsByMedium() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Leads By Medium",
      res_model: "crm.lead",
      domain: [
        ["type", "=", "lead"],
        ["user_id", "=", this.user_id],
      ],
      context: { group_by: "medium_id" },
      views: [[false, "list"]],
    });
  }

  async viewActivities() {
    let view = await this.orm.searchRead(
      "ir.model.data",
      [["name", "=", "crm_lead_view_list_activities"]],
      ["res_id"]
    );

    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "My Activities",
      res_model: "crm.lead",
      domain: [["activity_user_id", "=", this.user_id]],
      views: [[view.length > 0 ? view[0].res_id : false, "list"]],
    });
  }

  viewLeadsByMonth() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Leads By Month",
      res_model: "crm.lead",
      domain: [
        ["user_id", "=", this.user_id],
        ["type", "=", "lead"],
      ],
      context: {
        group_by: "create_date:month",
      },
      views: [[false, "list"]],
    });
  }

  viewLeadsByCampaign() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Leads By Campaign",
      res_model: "crm.lead",
      domain: [
        ["user_id", "=", this.user_id],
        ["type", "=", "lead"],
      ],
      context: {
        group_by: "campaign_id",
      },
      views: [[false, "list"]],
    });
  }

  viewLostLeadOpp() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Lost Lead/Opportunity",
      res_model: "crm.lead",
      domain: [
        ["type", "in", ["opportunity", "lead"]],
        ["user_id", "=", this.user_id],
        ["active", "=", false],
        ["probability", "=", 0],
      ],
      views: [[false, "list"]],
    });
  }
}

CRMDashboard.template = "dashboard_template";
CRMDashboard.components = { Card, ChartRenderer };

registry.category("actions").add("dashboard", CRMDashboard);
