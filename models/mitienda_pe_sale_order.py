from odoo import api, models, fields
from odoo.exceptions import ValidationError


class MiTiendaPeSaleOrder(models.Model):
    _name = "mitienda.pe.sale.order"
    _description = "Bitácora de sincronización de ventas"
    _rec_name = 'fecha_sincronizacion'
    _order = 'fecha_sincronizacion desc'

    conexion_id = fields.Many2one(string="Conexión", comodel_name="mitienda.pe.conexion", required=True)
    fecha_sincronizacion = fields.Datetime(string="Fecha de sincronización", required=True, default=fields.Datetime.now)
    fecha_venta = fields.Datetime(string='Fecha de venta')
    mensaje = fields.Char(string='Mensaje', required=True)
    sale_order_id = fields.Many2one(string="Venta", comodel_name="sale.order", ondelete="set null")
    partner_id = fields.Many2one(string="Cliente", comodel_name="res.partner", ondelete="set null")
    error = fields.Boolean(string='Estado', default=True)
    company_id = fields.Many2one(string="Compañia", comodel_name="res.company", required=True, default=lambda self: self.env.company)
    sync_cliente_logica = fields.Selection(
        string='Lógica de sincronización de cliente',
        selection=[
            ('registrar_nuevo', 'Nuevo cliente'),
            ('cliente_predefinido', 'Cliente predefinido'),
        ]
    )
    sync_cliente_predefinido = fields.Many2one(string='Cliente predefinido', comodel_name="res.partner", domain="[('company_id','=', company_id)]")
    sync_venta_logica = fields.Selection(
        selection=[
            ('cotizacion', 'Cotización'),
            ('venta', 'Venta'),
            ('factura_borrador', 'Venta con factura en borrador'),
            ('factura_publicada', 'Venta con factura publicada'),
        ],
        default="factura_publicada",
        string='Lógica de sincronización de venta'
    )
    mitienda_order_code = fields.Char(string='Código MiTienda')
    mitienda_order_id = fields.Integer(string='ID MiTienda')
    mitienda_order_status = fields.Selection(string="Estado MiTienda",
        selection=[('0','Rechazado'),('1', 'Aprobado'),('2', 'Pendiente'),('9', 'Creado')])
    mitienda_sunat_pdf = fields.Char(string='Factura SUNAT')
    mitienda_partner_id = fields.Many2one(string="Cliente MiTienda", comodel_name="mitienda.pe.partner", ondelete="set null")

    def unlink(self):
        for record in self:
            if record:
                raise ValidationError("No puede eliminar un registro")
        return super().unlink()
