from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    mitienda_id = fields.Integer(string="ID", copy=False)
    mitienda_email = fields.Char(string="Correo electrónico", copy=False)
    mitienda_doc_number = fields.Char(string="Número de documento", copy=False)
