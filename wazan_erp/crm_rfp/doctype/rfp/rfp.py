import frappe
from frappe import _
from frappe.model.document import Document


class RFP(Document):

    @frappe.whitelist()
    def submit_for_review(self):
        self._require("Draft")
        self.status = "In Review"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Submitted for review by {frappe.session.user}")
        frappe.msgprint(_("RFP submitted for review."))

    @frappe.whitelist()
    def approve(self):
        self._require("In Review")
        self.status = "Approved"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Approved by {frappe.session.user}")
        frappe.msgprint(_("RFP approved."))

    @frappe.whitelist()
    def reject(self):
        self._require("In Review")
        self.status = "Rejected"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Rejected by {frappe.session.user}")
        frappe.msgprint(_("RFP rejected."))

    def _require(self, expected):
        if self.status != expected:
            frappe.throw(_(f"Action requires status \'{expected}\'. Current: \'{self.status}\'"))
