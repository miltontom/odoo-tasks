{
    "name": "Requisition Management",
    "depends": ["base", "hr", "stock", "purchase", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "security/requisition_groups.xml",
        "views/hr_employee_views.xml",
        "views/requisition_request_views.xml",
        "views/requisition_request_line_views.xml",
        "views/requisition_menus.xml",
    ],
}
