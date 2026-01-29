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
            raise UserError(_("Configuración incompleta: Por favor, agrega la clave 'openai_api_key' en Ajustes > Técnico > Parámetros del sistema."))

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
                _logger.error(f"OpenAI Error: {response.text}")
                raise UserError(_("Error de OpenAI: Verifica tu saldo o la validez de tu clave."))
        except Exception as e:
            raise UserError(_("Error de conexión: %s") % str(e))

    # NOMBRES CORREGIDOS PARA COINCIDIR CON EL XML
    def action_generate_ai_description(self):
        for record in self:
            source = record.comment or record.name or "un nuevo contacto"
            ai_content = self._call_ai_api("Eres un asistente profesional.", f"Redacta un perfil profesional para: {source}")
            if ai_content:
                record.write({'comment': ai_content})

    def action_improve_ai_text(self):
        for record in self:
            if not record.comment:
                raise UserError(_("No hay texto en Notas Internas para mejorar."))
            edited = self._call_ai_api("Eres un editor experto.", f"Mejora la redacción de este texto: {record.comment}")
            if edited:
                record.write({'comment': edited})