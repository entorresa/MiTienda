from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mitienda_id = fields.Integer(string="ID", copy=False)
    mitienda_code = fields.Char(string="Código", copy=False)
    mitienda_sunat_pdf = fields.Char(string="Factura SUNAT", copy=False)
    mitienda_serie = fields.Char(string="Serie", copy=False)
    mitienda_correlative = fields.Char(string="Correlativo", copy=False)
    mitienda_nro_factura_sunat = fields.Char(string="Nro. Factura SUNAT", compute="_compute_mitienda_nro_factura_sunat", store=False)

    @api.depends('mitienda_serie','mitienda_correlative')
    def _compute_mitienda_nro_factura_sunat(self):
        for record in self:
            record.mitienda_nro_factura_sunat = '-'.join(x for x in [record.mitienda_serie, record.mitienda_correlative] if x)
