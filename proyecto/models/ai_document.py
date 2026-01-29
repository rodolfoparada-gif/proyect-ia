from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class IaDocument(models.Model):
    _name = 'ia.document'
    _description = 'Documento de Inteligencia Artificial'

    name = fields.Char(string='Título', required=True, default="Nuevo Documento")
    content = fields.Html(string='Contenido', sanitize=False)
    date_created = fields.Date(string='Fecha', default=fields.Date.today)

    def _call_ai_api(self, prompt_text):
        """ Conexión con el Endpoint de apifreellm.com """
        # Obtenemos su nueva API Key (la que empieza con apf_...)
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai_api_key')
        
        if not api_key:
            raise UserError(_("configure la nueva API Key en Parámetros del Sistema."))

        url = "https://apifreellm.com/api/v1/chat"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Estructura según la documentación de FreeLLM
        data = {
            "message": prompt_text,
            "model": "apifreellm"
        }

        try:
            # Enviamos la solicitud POST
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                res_data = response.json()
                # Extraemos 'response' del JSON recibido
                return res_data.get('response', 'Sin respuesta de la IA')
            
            elif response.status_code == 429:
                raise UserError(_("Límite alcanzado. Por favor espere 5 segundos."))
            
            elif response.status_code == 401:
                raise UserError(_("API Key de FreeLLM no válida. Verifíquela en Ajustes."))
                
            return False
        except Exception as e:
            _logger.error(f"Error en la conexión: {e}")
            return False

    def action_generate_info(self):
        """ Botón: CREAR INFORMACIÓN """
        for record in self:
            if not record.name or record.name == "Nuevo Documento":
                raise UserError(_("escriba un título para el documento."))
            
            prompt = f"Escribe un informe profesional y detallado sobre: {record.name}"
            res = self._call_ai_api(prompt)
            if res:
                record.content = res

    def action_edit_doc(self):
        """ Botón: MEJORAR TEXTO """
        for record in self:
            if not record.content:
                raise UserError(_("No hay contenido para mejorar, Mi Señor."))
            
            prompt = f"Mejora la redacción y ortografía del siguiente texto: {record.content}"
            res = self._call_ai_api(prompt)
            if res:
                record.content = res