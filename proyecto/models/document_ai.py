from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class IaDocument(models.Model):
    _name = 'ia.document'
    _description = 'Documento de Inteligencia Artificial'

    name = fields.Char(string='Título del Documento', required=True, default="Nuevo Documento")
    content = fields.Html(string='Contenido', sanitize=False)
    date_created = fields.Date(string='Fecha de Creación', default=fields.Date.today)

    def _call_ai_api(self, system_prompt, user_content):
        """ Función interna para conectar con OpenAI """
        # Buscamos la clave en Parámetros del Sistema
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai_api_key')
        
        if not api_key or api_key == 'sk-...':
            raise UserError(_("Mi Señor, no he encontrado su 'openai_api_key'. "
                            "Por favor, configúrela en Ajustes > Técnico > Parámetros del sistema."))

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
            # Timeout de 20 segundos por si la IA tarda en redactar
            response = requests.post(url, json=data, headers=headers, timeout=20)
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 401:
                raise UserError(_("Mi Señor, la API Key de OpenAI es inválida o ha expirado."))
            else:
                _logger.error(f"OpenAI Error: {response.text}")
                return False
        except requests.exceptions.Timeout:
            raise UserError(_("La conexión con OpenAI ha tardado demasiado. Intente nuevamente, Mi Señor."))
        except Exception as e:
            _logger.error(f"Error inesperado: {e}")
            return False

    def action_generate_info(self):
        """ 1. CREAR INFORMACIÓN: Usa el título para redactar contenido nuevo """
        for record in self:
            # Evitamos procesar si el título es el valor por defecto o está vacío
            if not record.name or record.name in ['Nuevo Documento', 'Nuevo']:
                raise UserError(_("Mi Señor, debe escribir un Título descriptivo para poder generar información."))
            
            _logger.info(f"Generando contenido para: {record.name}")
            
            system_msg = "Eres un redactor profesional y creativo. Genera textos largos, bien estructurados y en formato HTML."
            user_msg = f"Escribe un documento completo y profesional sobre el siguiente tema: {record.name}"
            
            res = self._call_ai_api(system_msg, user_msg)
            
            if res:
                record.write({'content': res})
            else:
                raise UserError(_("No he podido generar la información. Revise su conexión o saldo en OpenAI."))

    def action_edit_doc(self):
        """ 2. EDITAR DOCUMENTO: Toma el texto del campo 'content' y lo mejora """
        for record in self:
            # Validamos que exista contenido previo para mejorar
            if not record.content or len(record.content) < 10:
                raise UserError(_("El documento está vacío, Mi Señor. Primero use 'Crear Información' o escriba algo."))

            _logger.info(f"Mejorando documento ID: {record.id}")

            system_msg = "Eres un editor experto. Tu tarea es mejorar la redacción, corregir ortografía y dar un tono más profesional al texto, manteniendo el formato HTML."
            user_msg = f"Mejora el siguiente contenido: {record.content}"
            
            res = self._call_ai_api(system_msg, user_msg)
            
            if res:
                record.write({'content': res})
            else:
                raise UserError(_("No he podido editar el documento, Mi Señor."))