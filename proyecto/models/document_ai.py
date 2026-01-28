from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class AiContactEditor(models.Model):
    _inherit = 'res.partner' # Heredamos de Contactos

    def _call_ai_api(self, system_prompt, user_content):
        """Llamada centralizada a OpenAI usando parámetros del sistema"""
        
        # Buscamos la clave en Ajustes > Técnico > Parámetros del sistema
        # La clave real la pondrás tú manualmente en la interfaz de Odoo
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai_api_key')
        
        if not api_key:
            _logger.error("No se encontró la API Key de OpenAI en los parámetros del sistema.")
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
                return response.json()['choices'][0]['message']['content']
            else:
                _logger.error(f"Error en API IA: {response.text}")
                return False
        except Exception as e:
            _logger.error(f"Falla de conexión con la IA: {e}")
            return False

    def action_create_information(self):
        """Genera una descripción profesional basada en las notas actuales"""
        for record in self:
            source_text = record.comment or "un contacto nuevo"
            system_p = "Eres un asistente profesional que redacta perfiles de contactos."
            user_p = f"Crea una descripción profesional para este contacto basada en esto: {source_text}"
            
            ai_response = self._call_ai_api(system_p, user_p)
            if ai_response:
                record.write({'comment': ai_response})

    def action_edit_existing_content(self):
        """Mejora la redacción y ortografía del campo Notas"""
        for record in self:
            if record.comment:
                system_p = "Eres un editor experto en redacción corporativa."
                user_p = f"Mejora el estilo y ortografía de este texto: {record.comment}"
                
                edited = self._call_ai_api(system_p, user_p)
                if edited:
                    record.write({'comment': edited})