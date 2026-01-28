{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'category': 'Sales', # Cámbialo a 'Sales' temporalmente para que Odoo lo reconozca como App de negocio
    'author': 'Rodolfo Parada',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,    # ESTO ES LO QUE GENERA EL BOTÓN
    'auto_install': False,
    'license': 'LGPL-3',
}