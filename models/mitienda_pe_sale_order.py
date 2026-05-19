from odoo import api, models, fields
from odoo.exceptions import ValidationError


class MiTiendaPeSaleOrder(models.Model):
    _name = "mitienda.pe.sale.order"

    mitienda_partner_id = fields.Many2one(comodel_name="mitienda.pe.partner", string="Cliente MiTienda")
