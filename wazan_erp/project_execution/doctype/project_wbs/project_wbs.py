import frappe
from frappe import _
from frappe.model.document import Document

_LOCKED_FIELDS = ("description", "budget_amount", "source_bid")


class ProjectWBS(Document):

    def validate(self):
        if not self.is_new() and self.is_approved:
            original = frappe.get_doc("Project WBS", self.name)
            changed = [
                f for f in _LOCKED_FIELDS
                if getattr(self, f, None) != getattr(original, f, None)
            ]
            if changed:
                frappe.throw(_(
                    "Cannot modify {0} after WBS item has been approved."
                ).format(frappe.bold(", ".join(changed))))

    @frappe.whitelist()
    def approve(self):
        if self.is_approved:
            frappe.throw(_("WBS item is already approved."))
        self.is_approved = 1
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Approved and locked by {frappe.session.user}")
        frappe.msgprint(_("WBS item approved and locked."))
