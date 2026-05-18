from odoo import api, models, fields
from odoo.exceptions import ValidationError


class MiTiendaPeConexion(models.Model):
    _name = "mitienda.pe.conexion"
    _rec_name = 'url'

    url = fields.Char(string='API Host', required=True, default="https://api.mitienda.pe/v1")
    entorno = fields.Selection(string='Entorno', selection=[('pruebas', 'Pruebas'), ('produccion', 'Producción')], default='pruebas', required=True)
    token = fields.Char(string='Token API', required=True)
    token_expiracion = fields.Date(string='Expiración token')
    token_header = fields.Selection(string='Tipo de autenticación', selection=[('bearer', 'Bearer'), ('legacy', 'Lagacy')], default='bearer')
    timeout_api = fields.Integer(string='Timeout HTTP', required=True, default=30)
    activo = fields.Boolean(string='Activo', default=True)
    company_id = fields.Many2one(string='Compañía', comodel_name='res.company', default=lambda self: self.env.company.id, required=True)
    sync_cliente_logica = fields.Selection(string='Lógica de sincronización', required=True,
                                        selection=[('registrar_nuevo', 'Registrar nuevos clientes'),
                                                    ('cliente_predefinido', 'Usar cliente predefinido')], default='registrar_nuevo')
    sync_cliente_predefinido = fields.Many2one(comodel_name='res.partner', string='Cliente predefinido', domain="[('company_id','=', company_id)]")
    sync_venta_logica = fields.Selection(selection=[('cotizacion', 'Registrar cotizaciones'),
                                                    ('venta', 'Registrar ventas'),
                                                    ('factura_borrador', 'Registrar ventas y facturas en borrador'),
                                                    ('factura_publicada', 'Registrar ventas y facturas publicadas')],
                                        default="factura_publicada",
                                        string='Lógica de sincronización',
                                        required=True)
