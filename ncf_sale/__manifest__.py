

{
    'name': "NCF Sale",
    'version': '13.0.1.0.0',
    'summary': """
        Este módulo extiende la funcionalidad de NCF Manager hacia ventas,
        para realizar algunas validaciones antes de crear la factura.
    """,
    'author': "Astratech",
    'license': 'LGPL-3',
    'category': 'Localization',
    'external_dependencies': {
        'python': ['stdnum.do'],
    },

    # any module necessary for this one to work correctly
    'depends': ['ncf_manager', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
    ],
    'qweb': [],
  'installable': True,
}
