// Status colour map
const RFP_COLORS = {
    Draft: "blue",
    "In Review": "orange",
    Approved: "green",
    Rejected: "red",
};

frappe.ui.form.on("RFP", {
    refresh(frm) {
        frm.page.set_indicator(frm.doc.status, RFP_COLORS[frm.doc.status] || "grey");
        if (frm.is_new()) return;
        const s = frm.doc.status;
        if (s === "Draft")
            frm.add_custom_button(__("Submit for Review"), () =>
                frappe.confirm(__("Submit this RFP for review?"), () =>
                    frm.call("submit_for_review").then(() => frm.reload_doc())
                ), __("Action"));
        if (s === "In Review") {
            frm.add_custom_button(__("Approve"), () =>
                frm.call("approve").then(() => frm.reload_doc()), __("Action"));
            frm.add_custom_button(__("Reject"), () =>
                frappe.confirm(__("Reject this RFP?"), () =>
                    frm.call("reject").then(() => frm.reload_doc())
                ), __("Action"));
        }
    },
});
