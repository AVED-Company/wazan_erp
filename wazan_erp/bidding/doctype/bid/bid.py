import frappe
from frappe import _
from frappe.model.document import Document


def recalculate_totals(doc, method=None):
    """Called from hooks doc_events."""
    doc._recalculate()


class Bid(Document):

    def validate(self):
        self._recalculate()

    def _recalculate(self):
        gp      = (self.gp_percentage or 0) / 100
        overhead = (self.overhead_percentage or 0) / 100
        markup  = 1 + gp + overhead
        total_cost = total_price = 0

        for item in self.bid_items:
            item.total_cost = (
                (item.material_cost   or 0) +
                (item.labor_cost      or 0) +
                (item.equipment_cost  or 0) +
                (item.subcontract_cost or 0)
            )
            item.selling_price = item.total_cost * markup
            total_cost  += item.total_cost
            total_price += item.selling_price

        self.total_cost   = total_cost
        self.total_price  = total_price
        self.gross_margin = total_price - total_cost

    # ── Workflow actions ─────────────────────────────────────────────

    @frappe.whitelist()
    def submit_for_review(self):
        self._require("Draft")
        self.bid_status = "Internal Review"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Submitted for internal review by {frappe.session.user}")
        frappe.msgprint(_("Bid submitted for internal review."))

    @frappe.whitelist()
    def approve(self):
        self._require("Internal Review")
        self.bid_status = "Approved"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Approved by {frappe.session.user}")
        frappe.msgprint(_("Bid approved."))

    @frappe.whitelist()
    def mark_submitted(self):
        self._require("Approved")
        self.bid_status = "Submitted"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Bid submitted to client by {frappe.session.user}")
        frappe.msgprint(_("Bid marked as Submitted."))

    @frappe.whitelist()
    def mark_won(self):
        self._require("Submitted")
        self.bid_status = "Won"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Marked Won by {frappe.session.user}")
        frappe.msgprint(_("Congratulations — Bid Won!"))

    @frappe.whitelist()
    def mark_lost(self):
        self._require("Submitted")
        self.bid_status = "Lost"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Marked Lost by {frappe.session.user}")
        frappe.msgprint(_("Bid marked as Lost."))

    def _require(self, expected):
        if self.bid_status != expected:
            frappe.throw(_(f"Action requires status \'{expected}\'. Current: \'{self.bid_status}\'"))
