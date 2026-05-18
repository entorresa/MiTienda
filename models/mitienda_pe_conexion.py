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
    mensaje_sync_cliente = fields.Char(string="mensaje", compute='_mensaje_sync_cliente')

    @api.model
    def create(self, vals):
        if vals.get('url'):
            vals['url'] = vals['url'].rstrip('/')
        return super().create(vals)

    def write(self, vals):
        if vals.get('url'):
            vals['url'] = vals['url'].rstrip('/')
        return super().write(vals)

    @api.constrains('timeout_api', 'activo')
    def validacion(self):
        for record in self:
            if record.timeout_api <= 0:
                raise ValidationError("Timeout HTTP debe ser mayor a 0")
            conexiones = self.search([('id', '!=', record.id)])
            if record.activo and len(conexiones)>0:
                conexiones.write({'activo': False})

    @api.depends('sync_cliente_logica')
    def _mensaje_sync_cliente(self):
        for record in self:
            if record.sync_cliente_logica and record.sync_cliente_logica == 'registrar_nuevo':
                record.mensaje_sync_cliente = 'Se registran nuevos clientes tomando como base los datos de nombre, apellido, teléfono y correo electrónico'
            else:
                record.mensaje_sync_cliente = None

    def probar_conexion(self):
        return True

    def unlink(self):
        for record in self:
            if record.activo:
                raise ValidationError("No se puede eliminar un registro en estado activo")
        return super().unlink()