from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class AiDocumentEditor(models.Model):
    _inherit = 'note.note' # Heredamos de Notas [cite: 2]

    def _call_ai_api(self, system_prompt, user_content):
        """Llamada centralizada a OpenAI"""
        api_key = "TU_API_KEY_AQUI" # [cite: 3]
        url = "https://api.openai.com/v1/chat/completions" [cite: 3]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        } [cite: 3]

        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7
        } [cite: 4]

        try:
            response = requests.post(url, json=data, headers=headers, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'] [cite: 5]
            else:
                _logger.error(f"Error en API IA: {response.text}") [cite: 5]
                return False
        except Exception as e:
            _logger.error(f"Falla de conexión con la IA: {e}") [cite: 6]
            return False

    def action_create_information(self):
        """Genera información nueva"""
        for record in self:
            source_text = record.memo or "una nota nueva" [cite: 7]
            system_p = "Eres un asistente que crea información detallada y profesional." [cite: 7]
            user_p = f"Basado en este concepto, crea un documento completo: {source_text}" [cite: 8]
            
            ai_response = self._call_ai_api(system_p, user_p)
            if ai_response:
                record.write({'memo': ai_response}) [cite: 8]

    def action_edit_existing_content(self):
        """Mejora el contenido actual"""
        for record in self:
            if record.memo: [cite: 9]
                system_p = "Eres un editor profesional de documentos. Mejora la redacción y ortografía." [cite: 9]
                user_p = f"Corrige y mejora este texto: {record.memo}" [cite: 10]
                
                edited_content = self._call_ai_api(system_p, user_p)
                if edited_content:
                    record.write({'memo': edited_content}) [cite: 10]