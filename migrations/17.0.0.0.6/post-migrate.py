"""v0.0.6: users' default / allowed companies as on Clear-DB.

data/users_access_known_good.json had the known-good env's default companies for three users (Milinda,
Rohana, Tharaka), which differ from Clear-DB; it is applied only by post_init_hook. This re-applies the
companies (not the groups) to databases where the module is already installed, so sales-team memberships
that Clear-DB has (crm.team member company check) load.
"""
import json
import logging
import os

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                          'data', 'users_access_known_good.json')


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    Users = env['res.users'].sudo().with_context(active_test=False)
    with open(USERS_FILE, encoding='utf-8') as f:
        users = json.load(f)
    done = 0
    for u in users:
        user = Users.search([('login', '=', u['login'])], limit=1)
        companies = [c.id for c in (env.ref(x, raise_if_not_found=False) for x in u.get('companies', [])) if c]
        company = env.ref(u['company'], raise_if_not_found=False) if u.get('company') else None
        if not user or not companies:
            continue
        vals = {'company_ids': [(6, 0, companies)]}
        if company and company.id in companies:
            vals['company_id'] = company.id
        user.write(vals)
        done += 1
    _logger.info('known-good users: default / allowed companies re-applied for %d users', done)
