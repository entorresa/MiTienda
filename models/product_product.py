from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    mitienda_id = fields.Integer(string='ID')
    mitienda_sku = fields.Char(string='SKU')
