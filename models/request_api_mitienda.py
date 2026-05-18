from odoo import api, models, fields
from odoo.exceptions import ValidationError
import requests
import logging
_logger = logging.getLogger(__name__)

class RequestApiMiTienda(models.AbstractModel):
    _name = "request.api.mitienda"
    _description = 'Modelo para consumo API MiTienda'
    _auto = False


    company_id = fields.Many2one(comodel_name='res.company', string='Compañia')
    conexion_id = fields.Many2one(comodel_name='mitienda.pe.conexion', string="Conexión")
    cabecera = fields.Json(string="Cabecera", default=lambda self: {'Content-Type': 'application/json'})

    def init(self, company_id = None):
        self.company_id = company_id or self.env.company
        conexion_id = self.env['mitienda.pe.conexion'].search([('company_id','=', self.company_id.id),('activo','=', True)],limit=1)
        self.conexion_id = conexion_id
        if conexion_id:
            self.cabecera.update({'Authorization': f"Bearer {conexion_id.token}"} if conexion_id.token_header == 'Bearer' else {'token': conexion_id.token})
            return True
        else:
            _logger.error("No existe  una conexión activa para la compania seleccionada: %s", self.company_id.name)

    def request_api(self, endpoint, notificacion=False, mensaje='Éxito'):
        error = False
        data = {
            'success': False,
            'error': {
                'code': -1,
                'message': '',
            },
            'data': [],
            'meta': {},
        }
        try:
            if self.conexion_id.token_expiracion > fields.Datetime.now() or not self.conexion_id:
                data['error']['message'] = 'Token API expirado' if self.conexion_id.token_expiracion > fields.Datetime.now() else 'No se encontró una conexión activa'
            else:
                respuesta = requests.get(self.conexion_id.url + endpoint, headers=self.cabecera, timeout=self.conexion_id.timeout_api)
                respuesta.raise_for_status()
                data = respuesta.json()
        except Exception as e:
            data['error']['message'] = str(e)
        finally:
            if notificacion:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Éxito' if data.get('success') else 'Error',
                        'message': mensaje if data.get('success') else data.get('error', {}).get('message'),
                        'type': 'success' if data.get('success') else 'error',
                        'sticky': False,
                    },
                }
            else:
                return data


    def probar_conexion(self):
        endpoint = '/mitienda/paymentlinks'
        return self.request_api(endpoint, True, 'Conexión establecida')
