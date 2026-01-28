{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'author': 'Rodolfo Parada',
    'category': 'Productivity', # Categoría estándar para que sea fácil de encontrar
    'summary': 'Solución de Inteligencia Artificial para gestión de perfiles',
    'description': """
        App profesional para integrar OpenAI con Odoo.
        Permite generar y mejorar descripciones automáticamente.
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_view.xml',
    ],
    'installable': True,
    'application': True,    # OBLIGATORIO para que aparezca en el tablero de Apps
    'auto_install': False,
    'license': 'LGPL-3',
    'icon': '/proyecto/static/description/icon.png', # Ruta al icono de tu app
}