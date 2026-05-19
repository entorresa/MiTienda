from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mitienda_sale_order_id = fields.Many2one(string="Sincronización", comodel_name="mitienda.pe.sale.order")
    mitienda_id = fields.Integer(string="ID", readonly=True, related='mitienda_sale_order_id.mitienda_order_id')
    mitienda_code = fields.Char(string="Código", related="mitienda_sale_order_id.mitienda_order_code", readonly=True)
    mitienda_sunat_pdf = fields.Char(string="Factura SUNAT", related="mitienda_sale_order_id.mitienda_sunat_pdf", readonly=True)
