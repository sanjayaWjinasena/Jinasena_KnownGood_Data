# -*- coding: utf-8 -*-
{
    'name': 'Jinasena : Known-Good Data',
    'version': '17.0.0.0.2',
    'summary': 'Users & access, products, Knowledge, Website and Settings of Jinasena Agricultural '
               'Machinery, taken from the known-good env. For the new-install environment only.',
    'description': """
Jinasena : Known-Good Data
==========================

Data (not functionality) taken read-only from the known-good environment
(v17-final-39088506, company "Jinasena Agricultural Machinery (Pvt) Ltd." only),
for installing on the new-install environment only.

* data/*.csv, data/link/*.csv - hand-made security groups, products (UoM, categories,
  attributes, templates, attribute lines), Knowledge articles and covers, website pages
  with their views, shop categories, ribbons, FAQ records. Studio references were mapped
  to the repo records that replaced them (SHIPPED_ARTIFACTS.jsonl).
* data/res_config_settings_known_good.xml - the company's Settings, applied once at
  install like pressing Save (no app is installed or removed).
* data/users_access_known_good.json + hooks.py - internal users of the company and
  exactly the groups they have on known-good; missing users are created without a password.

Regenerate with scripts/_extract_master_data_kg.py, _extract_settings_kg.py,
_extract_users_kg.py and _assemble_known_good_module.py (PlayWrite Testings project).
""",
    'author': 'Jinasena Agricultural Machinery (Pvt) Ltd.',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'depends': ['seed_master_data_and_settings', 'BugFix-Studio-Misc', 'BugFix-Stock', 'studio_usermodel_migration', 'BugFix-Sales', 'BugFix-Purchase', 'crm', 'knowledge', 'website', 'website_sale'],
    'data': ['data/res.groups.csv', 'data/uom.category.csv', 'data/uom.uom.csv', 'data/product.category.csv', 'data/product.attribute.csv', 'data/product.attribute.value.csv', 'data/product.template.csv', 'data/product.template.attribute.line.csv', 'data/knowledge.cover.csv', 'data/knowledge_article_part_1/knowledge.article.csv', 'data/knowledge_article_part_2/knowledge.article.csv', 'data/knowledge_article_part_3/knowledge.article.csv', 'data/knowledge_article_part_4/knowledge.article.csv', 'data/ir.ui.view.csv', 'data/website.page.csv', 'data/product.public.category.csv', 'data/product.ribbon.csv', 'data/x_website_faqs.csv', 'data/x_website_faq.csv', 'data/link/res.groups.csv', 'data/link/product.attribute.value.csv', 'data/link/product.template.csv', 'data/link/knowledge.article.csv', 'data/link/product.public.category.csv', 'data/res_config_settings_known_good.xml'],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
    'application': False,
}
