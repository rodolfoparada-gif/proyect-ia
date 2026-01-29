{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'summary': 'Generador de contenido con IA',
    'category': 'Productivity',
    'author': 'Rodolfo Parada',
    'depends': ['base', 'mail', 'contacts'], # Indispensable para heredar vistas de contactos
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,    # Esto habilita el botón Instalar
    'auto_install': False,
    'license': 'LGPL-3',
}