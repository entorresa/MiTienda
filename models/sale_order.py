from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mitienda_id = fields.Integer(string="ID")
    mitienda_code = fields.Char(string="Código")
    mitienda_sunat_pdf = fields.Char(string="Factura SUNAT")

    mitienda_serie = fields.Char(string="Serie")
    mitienda_correlative = fields.Char(string="Correlativo")
    mitienda_nro_factura_sunat = fields.Char(string="Nro. Factura SUNAT", compute="_compute_mitienda_nro_factura_sunat")

    @api.depends('mitienda_serie','mitienda_correlative')
    def _compute_mitienda_nro_factura_sunat(self):
        for record in self:
            record.mitienda_nro_factura_sunat = f"{mitienda_serie} - {mitienda_correlative}"
