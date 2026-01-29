from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests

class IaDocument(models.Model):
    _name = 'ia.document'
    _description = 'Documento de Inteligencia Artificial'

    name = fields.Char(string='Título', required=True)
    content = fields.Html(string='Contenido', sanitize=False) # Usamos Html para un editor más rico
    date_created = fields.Date(string='Fecha', default=fields.Date.today)

    def _call_ai_api(self, system_prompt, user_content):
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai_api_key')
        if not api_key:
            raise UserError(_("Mi Señor, configure la 'openai_api_key' en Parámetros del Sistema."))

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        }
        try:
            response = requests.post(url, json=data, headers=headers, timeout=20)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return False
        except Exception:
            return False

    def action_generate_info(self):
        """ CREAR INFORMACIÓN """
        for record in self:
            res = self._call_ai_api("Eres un redactor profesional.", f"Escribe un informe sobre: {record.name}")
            if res:
                record.content = res

    def action_edit_doc(self):
        """ EDITAR DOCUMENTO """
        for record in self:
            if not record.content:
                raise UserError(_("El documento está vacío, Mi Señor."))
            res = self._call_ai_api("Eres un corrector de estilo.", f"Mejora este texto: {record.content}")
            if res:
                record.content = res