app_name        = "wazan_erp"
app_title       = "Wazan ERP"
app_publisher   = "Wazan"
app_description = "Construction ERP - Saudi Arabia"
app_email       = "manalerpnext@gmail.com"
app_license     = "MIT"

# ERPNext needed for Customer, Project, Opportunity, UOM links.
# Leave empty so the app installs on Frappe-only benches too.
required_apps = []

fixtures = [
    {"dt": "Role", "filters": [["role_name", "in", [
        "Sales Executive", "Estimation Engineer", "Operations Manager",
        "Project Manager", "Finance Manager", "QA QC Engineer", "Site Supervisor",
    ]]]},
]

# Doc Events
doc_events = {
    "Bid": {
        "validate": "wazan_erp.bidding.doctype.bid.bid.recalculate_totals",
    },
}
