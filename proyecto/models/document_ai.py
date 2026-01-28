from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class AiContactEditor(models.Model):
    _inherit = 'res.partner' # Ahora heredamos de Contactos

    def _call_ai_api(self, system_prompt, user_content):
        api_key = "TU_API_KEY_REAL" # Reemplaza con tu clave de OpenAI
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7
        }
        try:
            response = requests.post(url, json=data, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return False
        except Exception:
            return False

    def action_create_information(self):
        for record in self:
            source_text = record.comment or "un contacto nuevo"
            system_p = "Eres un asistente profesional."
            user_p = f"Crea una descripción profesional para este contacto: {source_text}"
            ai_response = self._call_ai_api(system_p, user_p)
            if ai_response:
                record.write({'comment': ai_response})

    def action_edit_existing_content(self):
        for record in self:
            if record.comment:
                system_p = "Eres un editor experto."
                user_p = f"Mejora este texto: {record.comment}"
                edited = self._call_ai_api(system_p, user_p)
                if edited:
                    record.write({'comment': edited})