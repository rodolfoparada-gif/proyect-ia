{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'author': 'Rodolfo Parada',
    'category': 'Tools',
    'summary': 'App independiente para gestión de perfiles con IA',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True, # Esto es clave para que aparezca como App
    'license': 'LGPL-3',
}