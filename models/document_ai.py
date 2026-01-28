from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class AiDocumentEditor(models.Model):
    _inherit = 'note.note' # Seguimos usando Notas como base

    def _call_ai_api(self, system_prompt, user_content):
        # Recupera la clave desde los parámetros del sistema de Odoo
        api_key = self.env['ir.config_parameter'].sudo().get_param('ia_editor.openai_api_key')
        
        if not api_key or api_key == "TU_API_KEY_AQUI":
            _logger.error("No se ha configurado la API Key en Ajustes > Parámetros del sistema")
            return False
            
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

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
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                _logger.error(f"Error en API IA: {response.text}")
                return False
        except Exception as e:
            _logger.error(f"Falla de conexión con la IA: {e}")
            return False

    def action_create_information(self):
        """Genera información nueva basada en el contenido actual o título"""
        for record in self:
            # Si el campo memo está vacío, usamos un texto base
            source_text = record.memo or "una nota nueva"
            system_p = "Eres un asistente que crea información detallada y profesional."
            user_p = f"Basado en este concepto, crea un documento completo: {source_text}"
            
            ai_response = self._call_ai_api(system_p, user_p)
            if ai_response:
                record.write({'memo': ai_response})

    def action_edit_existing_content(self):
        """Edita y mejora el contenido que ya existe"""
        for record in self:
            if record.memo:
                system_p = "Eres un editor profesional de documentos. Mejora la redacción y ortografía."
                user_p = f"Corrige y mejora este texto: {record.memo}"
                
                edited_content = self._call_ai_api(system_p, user_p)
                if edited_content:
                    record.write({'memo': edited_content})

    # Mantenemos esta por compatibilidad con tu botón anterior si lo deseas
    def action_generate_ai_content(self):
        self.action_edit_existing_content()