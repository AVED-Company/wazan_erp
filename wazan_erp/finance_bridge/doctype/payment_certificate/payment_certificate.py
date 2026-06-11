import frappe
from frappe import _
from frappe.model.document import Document


class PaymentCertificate(Document):

    def validate(self):
        self._calc_retention()
        self._validate_wir()

    def _calc_retention(self):
        if not self.contract:
            return
        ret_pct = frappe.db.get_value(
            "Construction Contract", self.contract, "retention_percentage"
        ) or 0
        self.retention_amount = (self.approved_amount or 0) * (ret_pct / 100)
        self.net_payment      = (self.approved_amount or 0) - self.retention_amount

    def _validate_wir(self):
        if not self.work_inspection_report:
            return
        wir_status = frappe.db.get_value(
            "Work Inspection Report", self.work_inspection_report, "status"
        )
        if wir_status != "Approved":
            frappe.throw(_(
                "Payment cannot proceed without an Approved Work Inspection Report. "
                "WIR {0} is currently \'{1}\'."
            ).format(
                frappe.bold(self.work_inspection_report), wir_status
            ))

    # ── Workflow actions ────────────────────────────────────────────

    @frappe.whitelist()
    def approve(self):
        self._require("Draft")
        self.status = "Approved"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Approved by {frappe.session.user}")
        frappe.msgprint(_("Payment Certificate approved."))

    @frappe.whitelist()
    def mark_paid(self):
        self._require("Approved")
        self.status = "Paid"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Marked as Paid by {frappe.session.user}")
        frappe.msgprint(_("Payment Certificate marked as Paid."))

    def _require(self, expected):
        if self.status != expected:
            frappe.throw(_(
                f"Action requires status \'{expected}\'. Current: \'{self.status}\'"
            ))
