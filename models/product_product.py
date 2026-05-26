from odoo import api, models, fields
from ..services.request_api_mitienda import RequestApiMiTienda

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
        if self.mitienda_sku and self.product_variant_count == 1:
            return self.product_variant_ids[0].verificar_sku()

class ProductProduct(models.Model):
    _inherit = "product.product"

    mitienda_id = fields.Integer(string='ID')
    mitienda_sku = fields.Char(string='SKU', tracking=True, copy=False)

    def verificar_sku(self):
        if self.mitienda_sku:
            respuesta = RequestApiMiTienda(self.env).buscar_producto(sku=self.mitienda_sku)
            if respuesta['success'] is True and self.mitienda_id != respuesta['data']['id']:
                self.write({'mitienda_id': respuesta['data']['id']})
            else:
                self.write({'mitienda_id': False})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error' if respuesta['success'] is False else 'Éxito',
                    'message': 'SKU verificado' if respuesta['success'] else respuesta['error']['message'],
                    'type': 'danger' if respuesta['success'] is False else 'success',
                    'sticky': False,
                    'next': {
                        'type': 'ir.actions.client',
                        'tag': 'soft_reload',
                    },
                },
            }
