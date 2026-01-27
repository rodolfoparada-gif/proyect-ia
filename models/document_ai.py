from odoo import models, fields, api
import requests # Para la llamada a la API

class AiDocumentEditor(models.Model):
    _inherit = 'note.note' # Extiende el modelo de Notas

    def action_generate_ai_content(self):
        for record in self:
            if not record.memo:
                continue

            # Configuración de la API (Ejemplo con OpenAI)
            # En producción, usa ir.config_parameter para la API Key
            api_key = "TU_API_KEY_AQUI"
            url = "https://api.openai.com/v1/chat/completions"
            
            headers = {º
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres un editor experto en Odoo."},
                    {"role": "user", "content": f"Mejora y expande este texto: {record.memo}"}
                ],
                "temperature": 0.7
            }

            try:
                response = requests.post(url, json=data, headers=headers, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    ai_text = result['choices'][0]['message']['content']
                    # Actualiza el campo de la nota con el texto de la IA
                    record.write({'memo': ai_text})
            except Exception as e:
                pass # Aquí podrías lanzar un aviso al usuario