

{
    'name': "NCF Purchase",
    'version': '13.0.1.0.0',
    'summary': """
    Add new field "Purchase Journal" in suppliers if this field is set
    the invoices generated for these suppliers take this journal by default.
    """,
    'author': "Astratech",
    'license': 'LGPL-3',
    'category': 'Localization',
    'depends': ['ncf_manager', 'purchase'],
    'data': ['views/res_partner_views.xml'],
  'installable': True,
}
