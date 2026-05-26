from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mitienda_id = fields.Integer(string='ID', compute='_compute_mitienda_id', inverse='_set_mitienda_id', store=True, copy=False)
    mitienda_sku = fields.Char(string='SKU', compute='_compute_mitienda_sku', inverse='_set_mitienda_sku', store=True, tracking=True, copy=False)

    @api.depends('product_variant_ids.mitienda_sku')
    def _compute_mitienda_sku(self):
        self._compute_template_field_from_variant_field('mitienda_sku')

    def _set_mitienda_sku(self):
        self._set_product_variant_field('mitienda_sku')

    @api.depends('product_variant_ids.mitienda_id')
    def _compute_mitienda_id(self):
        self._compute_template_field_from_variant_field('mitienda_id')

    def _set_mitienda_id(self):
        self._set_product_variant_field('mitienda_id')

    def _get_related_fields_variant_template(self):
        """ Return a list of fields present on template and variants models and that are related"""
        res = super()._get_related_fields_variant_template()
        res.extend(['mitienda_sku', 'mitienda_id'])
        return res

    def verificar_sku(self):
        return True

class ProductProduct(models.Model):
    _inherit = "product.product"

    mitienda_id = fields.Integer(string='ID')
    mitienda_sku = fields.Char(string='SKU', tracking=True, copy=False)

    def verificar_sku(self):
        return True