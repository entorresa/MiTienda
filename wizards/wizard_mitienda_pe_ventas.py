from odoo import api, models, fields
from odoo.exceptions import ValidationError
from ..services.request_api_mitienda import RequestApiMiTienda

class WizardMiTiendaPeVentas(models.TransientModel):
    _name = "wizard.mitienda.pe.ventas"
    _description = "wizard sincronización manual de ventas"

    conexion_id = fields.Many2one(string='Conexión', comodel_name="mitienda.pe.conexion")
    fecha_inicio = fields.Date(string="Fecha inicio", required=True, default= fields.Date.today())
    fecha_fin = fields.Date(string="Fecha fin", required=True, default=fields.Date.today())
    url = fields.Char(string='API Host', related='conexion_id.url', readonly=True)
    entorno = fields.Selection(string='Entorno', related='conexion_id.entorno', readonly=True)

    @api.constrains('fecha_inicio', 'fecha_fin')
    def validar(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError("Fecha inicio no debe superar a fecha fin")

    def sincronizar(self):
        return True

    @api.onchange('conexion_id')
    def conexion_onchange(self):
        if not self.conexion_id:
            return {
                'warning':{
                    'title': 'Error',
                    'message': 'Debe establecer una conexión activa para la compañía actual',
                }
            }

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        conexion = RequestApiMiTienda(self.env)
        if conexion.conexion_id:
            res['conexion_id'] = conexion.conexion_id.id
        return res