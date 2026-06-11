const BID_COLORS = {
    Draft: "blue",
    "Internal Review": "orange",
    Approved: "green",
    Submitted: "blue",
    Won: "green",
    Lost: "red",
};

frappe.ui.form.on("Bid", {
    refresh(frm) {
        frm.page.set_indicator(frm.doc.bid_status, BID_COLORS[frm.doc.bid_status] || "grey");
        if (frm.is_new()) return;
        const s = frm.doc.bid_status;
        if (s === "Draft")
            frm.add_custom_button(__("Submit for Review"), () =>
                frm.call("submit_for_review").then(() => frm.reload_doc()), __("Action"));
        if (s === "Internal Review")
            frm.add_custom_button(__("Approve"), () =>
                frm.call("approve").then(() => frm.reload_doc()), __("Action"));
        if (s === "Approved")
            frm.add_custom_button(__("Mark Submitted to Client"), () =>
                frm.call("mark_submitted").then(() => frm.reload_doc()), __("Action"));
        if (s === "Submitted") {
            frm.add_custom_button(__("Won ✓"), () =>
                frappe.confirm(__("Mark this bid as Won?"), () =>
                    frm.call("mark_won").then(() => frm.reload_doc())
                ), __("Action"));
            frm.add_custom_button(__("Lost"), () =>
                frappe.confirm(__("Mark this bid as Lost?"), () =>
                    frm.call("mark_lost").then(() => frm.reload_doc())
                ), __("Action"));
        }
    },
    gp_percentage:      frm => _recalc(frm),
    overhead_percentage: frm => _recalc(frm),
});

// Child table triggers
frappe.ui.form.on("Bid Item", {
    material_cost:    frm => _recalc(frm),
    labor_cost:       frm => _recalc(frm),
    equipment_cost:   frm => _recalc(frm),
    subcontract_cost: frm => _recalc(frm),
    bid_items_remove: frm => _recalc(frm),
});

function _recalc(frm) {
    const gp      = (frm.doc.gp_percentage || 0) / 100;
    const overhead = (frm.doc.overhead_percentage || 0) / 100;
    const markup  = 1 + gp + overhead;
    let tc = 0, tp = 0;

    (frm.doc.bid_items || []).forEach(r => {
        r.total_cost    = (r.material_cost || 0) + (r.labor_cost || 0) +
                          (r.equipment_cost || 0) + (r.subcontract_cost || 0);
        r.selling_price = r.total_cost * markup;
        tc += r.total_cost;
        tp += r.selling_price;
    });

    frm.set_value("total_cost",   tc);
    frm.set_value("total_price",  tp);
    frm.set_value("gross_margin", tp - tc);
    frm.refresh_field("bid_items");
}
