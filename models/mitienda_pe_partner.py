from odoo import api, models, fields
from odoo.exceptions import ValidationError


class MiTiendaPePartner(models.Model):
    _name = "mitienda.pe.partner"
    _rec_name = 'fecha_sincronizacion'
    _order = 'fecha_sincronizacion desc'

    conexion_id = fields.Many2one(string="Conexión", comodel_name="mitienda.pe.conexion", required=True)
    mitienda_sale_order_ids = fields.One2many(string="Ventas", comodel_name="mitienda.pe.sale.order", inverse_name="mitienda_partner_id")
    fecha_sincronizacion = fields.Datetime(string="Fecha de sincronización", required=True, default=fields.Datetime.now)
    company_id = fields.Many2one(string="Compañia", comodel_name="res.company", required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one(string="Cliente", comodel_name="res.partner", required=True)
    mitienda_name = fields.Char(string="Nombres")
    mitienda_last_name = fields.Char(string="Apellidos")
    mitienda_email = fields.Char(string="Correo electrónico")
    mitienda_doc_number = fields.Char(string="Documento")

    def unlink(self):
        for record in self:
            if record:
                raise ValidationError("No puede eliminar un registro")
        return super().unlink()
