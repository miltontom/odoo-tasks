{
    "name": "Vehicle Repair",
    "version": "1.0",
    "depends": [
        "base",
        "fleet",
        "hr_hourly_cost",
        "sale_management",
        "contacts",
        "mail",
        "website",
        "web",
    ],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/vehicle_repair_data.xml",
        "data/tag_data.xml",
        "data/labor_cost_data.xml",
        "data/email_template.xml",
        "data/automations.xml",
        "wizard/create_report_views.xml",
        "report/vehicle_repair_reports.xml",
        "report/vehicle_repair_report_templates.xml",
        "views/vehicle_repair_views.xml",
        "views/tag_views.xml",
        "views/labor_cost_views.xml",
        "views/consumed_part_views.xml",
        "views/res_partner_views.xml",
        "views/duplicate_record_error_template.xml",
        "views/card_info.xml",
        "views/website_menus.xml",
        "views/vehicle_repair_menus.xml",
        "views/website_repair_request_template.xml",
        "views/repair_requests_template.xml",
        "views/contact_request_template.xml",
        "views/snippets/top_repairs_template.xml",
        "views/snippets/website_snippets_inherit_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "vehicle_repair/static/src/xml/top_repairs_templates.xml",
            "vehicle_repair/static/src/js/underscore.js",
            "vehicle_repair/static/src/js/website_snippet.js",
        ],
        "web.assets_backend": [
            "vehicle_repair/static/src/js/action_manager.js",
        ],
    },
}



























