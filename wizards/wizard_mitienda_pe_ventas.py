from odoo import api, models, fields
from odoo.exceptions import ValidationError


class WizardMiTiendaPeVentas(models.TransientModel):
    _name = "wizard.mitienda.pe.ventas"
    _description = "wizard sincronización manual de ventas"

    conexion_id = fields.Many2one(string='Conexión', comodel_name="mitienda.pe.conexion")
    fecha_inicio = fields.Date(string="Fecha inicio", required=True, default= fields.Date.today())
    fecha_fin = fields.Date(string="Fecha fin", required=True, default=fields.Date.today())
    url = fields.Char(string='API Host', related='conexion_id.url', readonly=True)
    entorno = fields.Selection(string='Entorno', related='conexion_id.entorno', readonly=True)

    def sincronizar(self):
        return True
