frappe.ui.form.on("Project WBS", {
    refresh(frm) {
        if (frm.doc.is_approved) {
            frm.dashboard.add_indicator(__("Approved — Locked"), "green");
        }
        if (!frm.is_new() && !frm.doc.is_approved) {
            frm.add_custom_button(__("Approve & Lock"), () =>
                frappe.confirm(__("Approve this WBS item? Key fields will be locked."), () =>
                    frm.call("approve").then(() => frm.reload_doc())
                ), __("Action"));
        }
    },
});
