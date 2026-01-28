{
    'name': 'IA Editor Pro',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'IA para potenciar documentos y correos',
    
    # AQUÍ ES DONDE "HEREDAS" O DEPENDES DE OTROS MÓDULOS
    'depends': [
        'base',      # Requerido siempre
        'mail',      # Para heredar del chatter y mensajes
        'note',      # Si quieres usarlo en Notas (como el ejemplo anterior)
    ],

    'data': [
        'views/ai_view.xml',
    ],
    'installable': True,
}