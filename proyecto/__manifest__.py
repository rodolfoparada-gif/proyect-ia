
# {
#     'name': 'IA Editor Pro',
#     'version': '1.1',
#     'summary': 'Herramienta exclusiva para Crear y Editar Información con IA',
#     'category': 'Productivity',
#     'author': 'Rodolfo Parada',
#     'depends': ['base', 'contacts'],
#     'data': [
#         'security/ir.model.access.csv',
#         'views/ai_view.xml',
#     ],
#     'installable': True,
#     'application': True,
#     'license': 'LGPL-3',
# }

{
    'name': 'IA Editor Pro',
    'version': '1.2',
    'summary': 'Editor de documentos independiente con IA',
    'category': 'Tools',
    'author': 'Rodolfo Parada',
    'depends': ['base'], # Eliminamos 'contacts'
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}