from odoo import api, models, fields


class MiTiendaPeProduct(models.Model):
    _name = "mitienda.pe.product"
    _description = "Bitácora de sincronización de stock"
    _order = "fecha_sincronizacion desc"
    _rec_name = "fecha_sincronizacion"

    conexion_id = fields.Many2one(string="Conexión", comodel_name="mitienda.pe.conexion", required=True)
    product_template_id = fields.Many2one(string="Producto", comodel_name="product.template")
    product_product_id = fields.Many2one(string="Variante", comodel_name="product.product")
    fecha_sincronizacion = fields.Datetime(string="Fecha de sincronización", default=fields.Datetime.now)
    company_id = fields.Many2one(string="Compañía", comodel_name="res.company", required=True, default=lambda self: self.env.company)
    stock_picking_id = fields.Many2one(string="Operación de albarán", comodel_name="stock.picking")
    stock_inicial = fields.Float(string="Stock inicial")
    stock_ajuste = fields.Float(string="Incremento/Decremento")
    stock_final = fields.Float(string="Stock final", compute="_calcular_stock_final", store=True)
    mitienda_id = fields.Integer(string="ID MiTienda", related="product_product_id.mitienda_id")
    mitienda_sku = fields.Char(string="SKU", related="product_product_id.mitienda_sku")

    @api.depends('stock_inicial', 'stock_ajuste')
    def _calcular_stock_final(self):
        for record in self:
            record.stock_final =  record.stock_inicial + record.stock_ajuste

