{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'summary': 'Generador de contenido inteligente',
    'category': 'Productivity', # Cambia a esta categoría oficial
    'author': 'Rodolfo Parada',
    'depends': ['base', 'mail','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,    # ESTO HACE QUE APAREZCA EL BOTÓN INSTALAR
    'auto_install': False,  # Evita que se instale solo
    'license': 'LGPL-3',
}

