from odoo import api, models, fields
from odoo.exceptions import ValidationError


class RequestApiMiTienda(models.AbstractModel):
    _name = "request.api.mitienda"
    _description = 'Modelo para consumo API MiTienda'
    _auto = False


    company_id = fields.Many2one(comodel_name='res.company', string='Compañia')
    conexion_id = fields.Many2one(comodel_name='mitienda.pe.conexion', string="Conexión")
    cabecera = fields.Json(string="Cabecera", default=lambda self: {'Content-Type': 'application/json'})

    def init(self, company_id = None):
        