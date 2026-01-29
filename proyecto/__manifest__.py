
{
    'name': 'IA Editor Pro',
    'version': '1.2',
    'summary': 'Editor de documentos independiente con IA',
    # 'category': 'Tools',
     'category': 'Productivity',
    'author': 'Rodolfo Parada',
    'depends': ['base','web'], # Eliminamos 'contacts'
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}