

{
    'name': 'IA Editor Pro',
    'version': '1.2',
    'summary': 'Editor de documentos independiente con IA',
    'category': 'Tools',
    'author': 'Rodolfo Parada',
    'depends': ['base', 'web'], # 'web' es vital en producción
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}