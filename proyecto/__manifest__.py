{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'author': 'Rodolfo Parada',
    'category': 'Tools',
    'summary': 'Genera y edita contenido usando IA en Contactos',
    'depends': ['base', 'mail'], # Usamos solo lo esencial
    'data': [
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}