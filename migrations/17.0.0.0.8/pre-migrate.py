"""v0.0.8: pin the seeded knowledge.article records as noupdate so they stop being re-imported.

Why this exists
---------------
data/knowledge_article_part_*/knowledge.article.csv carry each article's members
as one2many sub-columns:

    article_member_ids/partner_id/id , article_member_ids/permission

Two of the 130 seeded articles use them, both granting ``write`` to
``base.partner_admin`` (``knowledge_article_odoo_documentation`` and
``knowledge_article_customized_pump_packages_faqs``). Those member lines get no
XML id of their own, so a re-import cannot match the line it wrote last time: it
creates a second one, and knowledge rejects it.

    duplicate key value violates unique constraint
        "knowledge_article_member_unique_article_partner"
    DETAIL: Key (article_id, partner_id)=(252, 3) already exists.

The member cannot simply be dropped from the CSV: both articles have
``internal_permission = 'read'``, and knowledge's ``_check_is_writable``
constraint requires an article that does not inherit write to have a member with
write access. It cannot be moved to a separate file either -- the constraint
runs when the article is created, so on a fresh install the member has to arrive
with the article, in the same import.

Deleting the stored members before the import is not an option either: article
permissions are inherited, and the articles seeded in part_1 take their write
access from the parent whose member would be gone. part_1 is imported before the
part_2/part_4 rows that would restore it, so the whole load fails with

    The article '... Data Upload Initial Setup' needs at least one member
    with 'Write' access.

Fix
---
Set ``noupdate`` on the ir_model_data rows of the seeded articles. ``_load_records``
skips a record whose xmlid is flagged noupdate when loading in update mode
(``if not (update and d_noupdate)``), so the articles -- and with them the member
sub-columns -- are no longer rewritten on upgrade. The stored rows stay exactly
as they are, which is the intent of a known-good snapshot: it seeds a database
once, it is not a source of continuous updates.

Fresh installs are covered from hooks.py (``pin_seeded_articles``), which flags
the same rows right after they are first created.

Idempotent: re-running only re-flags rows that are already flagged.
"""

import logging

_logger = logging.getLogger(__name__)

MODULE = "Jinasena_KnownGood_Data"


def migrate(cr, version):
    if not version:
        return

    cr.execute(
        """
        UPDATE ir_model_data
           SET noupdate = true
         WHERE module = %s
           AND model = 'knowledge.article'
           AND noupdate IS NOT TRUE
     RETURNING name
        """,
        (MODULE,),
    )
    pinned = cr.fetchall()
    if pinned:
        _logger.info(
            "Pinned %s seeded knowledge.article record(s) as noupdate so the CSV "
            "re-import no longer duplicates their article_member_ids lines",
            len(pinned),
        )
