"""v0.0.9: product types from Clear-DB on databases seeded before the type column existed.

Up to v0.0.8 data/product.template.csv had no detailed_type, so every seeded product was created as a
consumable. v0.0.9 adds the column; re-importing it would change the type of products already used in
stock moves, which Odoo refuses ("You can not change the type of a product that was already used"), so
the upgrade would stop. This sets the type first, directly, for this module's own products that are
consumables here and storable / service in the CSV; the import then writes the same value. On databases
where the types already match (Clear-DB copies) it does nothing.
"""

import csv
import logging
import os

_logger = logging.getLogger(__name__)

MODULE = "Jinasena_KnownGood_Data"


def migrate(cr, version):
    if not version:
        return
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "product.template.csv",
    )
    csv.field_size_limit(1 << 30)
    with open(path, encoding="utf-8-sig", newline="") as fh:
        want = {
            r["id"]: r["detailed_type"]
            for r in csv.DictReader(fh)
            if r.get("detailed_type")
        }
    cr.execute(
        "SELECT d.name, t.id FROM ir_model_data d JOIN product_template t ON t.id = d.res_id "
        "WHERE d.module = %s AND d.model = 'product.template' AND t.detailed_type = 'consu'",
        (MODULE,),
    )
    todo = {}
    for name, tid in cr.fetchall():
        target = want.get(name)
        if target in ("product", "service"):
            todo.setdefault(target, []).append(tid)
    for target, ids in todo.items():
        cr.execute(
            "UPDATE product_template SET detailed_type = %s, type = %s WHERE id = ANY(%s)",
            (target, target, ids),
        )
        _logger.info(
            "%s: %s seeded products set to %s (Clear-DB type)", MODULE, len(ids), target
        )
