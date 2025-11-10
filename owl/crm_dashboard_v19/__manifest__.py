{
    "name": "CRM Dashboard",
    "depends": ["base", "crm", "account", "sale_management"],
    "data": ["views/crm_dashboard.xml"],
    "assets": {
        "web.assets_backend": [
            "crm_dashboard/static/src/**/*",
        ]
    },
}
