from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mitienda_id = fields.Integer(string="ID")
    mitienda_code = fields.Char(string="Código")
    mitienda_sunat_pdf = fields.Char(string="Factura SUNAT")
