from odoo import api, models, fields
from odoo.exceptions import ValidationError
from ..services.request_api_mitienda import RequestApiMiTienda
from ..services.sync_api_mitienda import SyncAPIMiTienda

class WizardMiTiendaPeVentas(models.TransientModel):
    _name = "wizard.mitienda.pe.ventas"
    _description = "Sincronización manual de ventas"

    conexion_id = fields.Many2one(string='Conexión', comodel_name="mitienda.pe.conexion")
    fecha_inicio = fields.Date(string="Fecha inicio", required=True, default= fields.Date.today())
    fecha_fin = fields.Date(string="Fecha fin", required=True, default=fields.Date.today())
    url = fields.Char(string='API Host', related='conexion_id.url', readonly=True)
    entorno = fields.Selection(string='Entorno', related='conexion_id.entorno', readonly=True)

    @api.constrains('fecha_inicio', 'fecha_fin')
    def validar(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError("Fecha inicio debe ser igual o anterior a fecha fin")

    def sincronizar(self):
        return SyncAPIMiTienda(self.env).sincronizar_ventas(fecha_inicio=self.fecha_inicio, fecha_fin=self.fecha_fin)

    def default_get(self, fields_list):
        conexion = RequestApiMiTienda(self.env)
        if conexion.conexion_id:
            res = super().default_get(fields_list)
            res['conexion_id'] = conexion.conexion_id.id
            return res
        raise ValidationError('Debe establecer una conexión activa para la compañía actual')
