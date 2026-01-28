{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'author': 'Rodolfo Parada',
    'category': 'Tools',
    'summary': 'Genera y edita contenido usando IA en Contactos para todo el equipo',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv', # ARCHIVO NUEVO
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}