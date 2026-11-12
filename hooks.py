# -*- coding: utf-8 -*-
"""Users + group access from the known-good env (company 2), applied at install.

data/users_access_known_good.json lists every internal user allowed in Jinasena Agricultural
Machinery on the known-good env: login, name, default company, allowed companies and the
groups they are in (record names that exist once all MasterData modules are installed).
Missing users are created without a password (set one or send an invitation afterwards);
every listed user gets exactly the groups and companies they have on known-good. ORM only.
"""
import json
import logging
import os

_logger = logging.getLogger(__name__)
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'users_access_known_good.json')


def apply_known_good_users(env):
    with open(USERS_FILE, encoding='utf-8') as f:
        users = json.load(f)
    Users = env['res.users'].sudo().with_context(active_test=False, no_reset_password=True)
    created = updated = 0
    for u in users:
        companies = [c.id for c in (env.ref(x, raise_if_not_found=False) for x in u['companies']) if c]
        company = env.ref(u['company'], raise_if_not_found=False) if u.get('company') else None
        groups, missing = [], []
        for x in u['groups']:
            g = env.ref(x, raise_if_not_found=False)
            (groups.append(g.id) if g else missing.append(x))
        if missing:
            _logger.warning("known-good users: %s - groups not found, skipped: %s", u['login'], missing)
        vals = {'groups_id': [(6, 0, groups)]}
        if companies:
            vals['company_ids'] = [(6, 0, companies)]
            if company and company.id in companies:
                vals['company_id'] = company.id
        user = Users.search([('login', '=', u['login'])], limit=1)
        if user:
            user.write(vals)
            updated += 1
        else:
            Users.create(dict(vals, name=u['name'], login=u['login'], active=u.get('active', True)))
            created += 1
    _logger.info("known-good users: %d created, %d updated", created, updated)


def pin_seeded_articles(env):
    """Flag the seeded knowledge.article records noupdate so they are imported once.

    data/knowledge_article_part_*/knowledge.article.csv build each article's
    members from one2many sub-columns (article_member_ids/partner_id/id and
    .../permission). Those member lines carry no XML id, so a later re-import
    cannot match the line it wrote and inserts a second one instead, which
    knowledge rejects:

        duplicate key value violates unique constraint
            "knowledge_article_member_unique_article_partner"

    The member has to stay inline -- the two articles that have one are
    internal_permission='read', and _check_is_writable demands a write member
    at creation time -- so the import itself is made one-shot instead.
    _load_records skips a noupdate xmlid in update mode, which is the right
    semantics for a known-good snapshot: it seeds a database once.

    migrations/17.0.0.0.7/pre-migrate.py does the same for databases that were
    already installed before this was added.
    """
    env.cr.execute(
        """
        UPDATE ir_model_data
           SET noupdate = true
         WHERE module = %s
           AND model = 'knowledge.article'
           AND noupdate IS NOT TRUE
        """,
        ("Jinasena_KnownGood_Data",),
    )
    _logger.info("known-good: pinned %d seeded knowledge.article record(s) as noupdate",
                 env.cr.rowcount)


def post_init_hook(env):
    apply_known_good_users(env)
    pin_seeded_articles(env)
