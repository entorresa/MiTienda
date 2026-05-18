from odoo import api, models, fields
from odoo.exceptions import ValidationError
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
        conexion_id = self.env['mitienda.pe.conexion'].search([('company_id','=', self.company_id),('activo','=', True)],limit=1)
        self.conexion_id = conexion_id
        if conexion_id:
            self.cabecera.update({'Authorization': f"Bearer {conexion_id.token}"} if conexion_id.token_header == 'Bearer' else {'token': conexion_id.token})
            return True
        else:
            _logger.error("No existe  una conexión activa para la compania seleccionada: %s", self.company_id.name)
