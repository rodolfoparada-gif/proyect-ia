from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class AiContactEditor(models.Model):
    _inherit = 'res.partner'

    def _call_ai_api(self, system_prompt, user_content):
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai_api_key')
        if not api_key:
            raise UserError(_("Mi Señor, debe configurar la 'openai_api_key' en Parámetros del Sistema."))

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
            return False
        except Exception as e:
            _logger.error(f"Error IA: {e}")
            return False

    def action_generate_ai_description(self):
        """ Función para CREAR INFORMACIÓN """
        for record in self:
            source = record.name or "documento"
            res = self._call_ai_api("Eres un redactor experto.", f"Crea una descripción profesional detallada para: {source}")
            if res:
                record.comment = res

    def action_improve_ai_text(self):
        """ Función para EDITAR/MEJORAR DOCUMENTO """
        for record in self:
            if not record.comment:
                raise UserError(_("No hay contenido que editar, Mi Señor."))
            res = self._call_ai_api("Eres un editor de estilo.", f"Mejora profesionalmente este texto: {record.comment}")
            if res:
                record.comment = res