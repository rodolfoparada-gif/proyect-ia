from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import time # Para manejar el delay de 5 segundos si es necesario

class IaDocument(models.Model):
    _name = 'ia.document'
    _inherit = ['ia.document'] # Mantenemos lo anterior

    def _call_ai_api(self, system_prompt, user_content):
        """ Conexión con API Free LLM """
        # Buscamos la nueva API Key en Parámetros del Sistema
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai_api_key')
        
        if not api_key:
            raise UserError(_("configure su nueva API Key de FreeLLM en Parámetros del Sistema."))

        url = "https://apifreellm.com/api/v1/chat"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Combinamos el sistema y el usuario ya que esta API usa un mensaje simple
        full_message = f"{system_prompt}\n\nPregunta: {user_content}"
        
        data = {
            "message": full_message,
            "model": "apifreellm"
        }

        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                res_json = response.json()
                # Según el ejemplo, el texto viene en la clave 'response'
                return res_json.get('response')
            
            elif response.status_code == 429:
                raise UserError(_("debemos esperar 5 segundos (Límite del plan gratis)."))
            
            elif response.status_code == 401:
                raise UserError(_("La API Key de FreeLLM no es válida."))
            
            return False
        except Exception:
            return False