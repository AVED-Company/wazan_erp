const WIR_COLORS = {Pending: "orange", Approved: "green", Rejected: "red"};

frappe.ui.form.on("Work Inspection Report", {
    refresh(frm) {
        frm.page.set_indicator(frm.doc.status, WIR_COLORS[frm.doc.status] || "grey");
        if (frm.is_new()) return;
        if (frm.doc.status === "Pending") {
            frm.add_custom_button(__("Approve"), () =>
                frappe.confirm(__("Approve this inspection?"), () =>
                    frm.call("approve").then(() => frm.reload_doc())
                ), __("Action"));
            frm.add_custom_button(__("Reject"), () =>
                frappe.confirm(__("Reject this inspection?"), () =>
                    frm.call("reject").then(() => frm.reload_doc())
                ), __("Action"));
        }
    },
});
