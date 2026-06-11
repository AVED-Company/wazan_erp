const PAY_COLORS = {Draft: "blue", Approved: "green", Paid: "green"};

frappe.ui.form.on("Payment Certificate", {
    refresh(frm) {
        frm.page.set_indicator(frm.doc.status, PAY_COLORS[frm.doc.status] || "grey");
        if (frm.is_new()) return;
        if (frm.doc.status === "Draft")
            frm.add_custom_button(__("Approve"), () =>
                frappe.confirm(__("Approve this payment certificate?"), () =>
                    frm.call("approve").then(() => frm.reload_doc())
                ), __("Action"));
        if (frm.doc.status === "Approved")
            frm.add_custom_button(__("Mark as Paid"), () =>
                frappe.confirm(__("Mark this certificate as Paid?"), () =>
                    frm.call("mark_paid").then(() => frm.reload_doc())
                ), __("Action"));
    },

    approved_amount(frm) {
        // Client-side retention preview
        if (!frm.doc.contract) return;
        frappe.db.get_value("Construction Contract", frm.doc.contract, "retention_percentage")
            .then(r => {
                const pct = r.message?.retention_percentage || 0;
                const ret = (frm.doc.approved_amount || 0) * pct / 100;
                frm.set_value("retention_amount", ret);
                frm.set_value("net_payment", (frm.doc.approved_amount || 0) - ret);
            });
    },
});
