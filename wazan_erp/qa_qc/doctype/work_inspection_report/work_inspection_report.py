import frappe
from frappe import _
from frappe.model.document import Document


class WorkInspectionReport(Document):

    @frappe.whitelist()
    def approve(self):
        self._require("Pending")
        self.status = "Approved"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Inspection approved by {frappe.session.user}")
        frappe.msgprint(_("Work Inspection Report approved."))

    @frappe.whitelist()
    def reject(self):
        self._require("Pending")
        self.status = "Rejected"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Inspection rejected by {frappe.session.user}")
        frappe.msgprint(_("Work Inspection Report rejected."))

    def _require(self, expected):
        if self.status != expected:
            frappe.throw(_(
                f"Action requires status \'{expected}\'. Current: \'{self.status}\'"
            ))
