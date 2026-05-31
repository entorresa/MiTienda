from odoo import api, models, fields
from ..services.request_api_mitienda import RequestApiMiTienda
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        try:
            res = super().button_validate()
            for picking in self:
                if picking.state == 'done' and (not picking.sale_id or (picking.sale_id.mitienda_id == 0 and not picking.sale_id.mitienda_code)) and picking.location_id.id != picking.location_dest_id.id:
                    conexion = RequestApiMiTienda(picking.env)
                    for line in picking.move_ids:
                        if line.product_id.is_storable and line.product_id.mitienda_sincronizar_stock and (line.product_id.mitienda_id != 0 or line.product_id.mitienda_sku):
                            if picking.picking_type_id.code == 'incoming' or picking.picking_type_id.code == 'outgoing':
                                respuesta = conexion.buscar_producto(id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
                                if respuesta['success'] is True:
                                    stock_inicial = respuesta['data']['stock']
                                    if picking.picking_type_id.code == 'incoming':
                                        stock_ajuste = line.quantity
                                        stock_ajuste_prueba = -line.quantity
                                    elif picking.picking_type_id.code == 'outgoing':
                                        stock_ajuste = -line.quantity
                                        stock_ajuste_prueba = line.quantity
                                    stock = stock_inicial + stock_ajuste
                                    stock_prueba = stock
                                    if stock < 0:
                                        stock=0
                                    datos = {'stock': stock}
                                    respuesta2 = conexion.actualizar_producto(datos=datos, id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
                                    if respuesta2['success'] is True:
                                        self.registrar_bitacora_producto(conexion_id=conexion.conexion_id.id,
                                                                            product_temp_id=line.product_id.product_tmpl_id.id,
                                                                            product_product_id=line.product_id.id,
                                                                            picking_id=picking.id,
                                                                            stock_inicial= stock_inicial,
                                                                            stock_ajuste= stock_ajuste,
                                                                            mitienda_id= respuesta['data']['id'],
                                                                            mitienda_sku= respuesta['data']['sku'])
                                        if conexion.conexion_id.entorno == 'pruebas':
                                            datos = {'stock': stock_inicial}
                                            _logger.info(f"Restaurando stock de: {stock} a: {stock_inicial}")
                                            respuesta2 = conexion.actualizar_producto(datos=datos, id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
                                            if respuesta2['success'] is True:
                                                self.registrar_bitacora_producto(conexion.conexion_id.id,
                                                                                    product_temp_id = line.product_id.product_tmpl_id.id,
                                                                                    product_product_id = line.product_id.id,
                                                                                    picking_id = picking.id,
                                                                                    stock_inicial = stock_prueba,
                                                                                    stock_ajuste = stock_ajuste_prueba,
                                                                                    mitienda_id = respuesta['data']['id'],
                                                                                    mitienda_sku = respuesta['data']['sku'])
                                    else:
                                        if respuesta2['success'] is False:
                                            _logger.error(respuesta2['error']['message'])
            return res
        except Exception as e:
            _logger.error(str(e))

    def registrar_bitacora_producto(self, conexion_id=None, product_temp_id=None, product_product_id=None, picking_id=None, stock_inicial=0, stock_ajuste=0, mitienda_id=None, mitienda_sku=None):
        self.env['mitienda.pe.product'].create({
            'conexion_id': conexion_id,
            'product_template_id': product_temp_id,
            'product_product_id': product_product_id,
            'fecha_sincronizacion': fields.Datetime.now(),
            'company_id': self.env.company.id,
            'stock_picking_id': picking_id,
            'stock_inicial': stock_inicial,
            'stock_ajuste': stock_ajuste,
            'mitienda_id': mitienda_id,
            'mitienda_sku': mitienda_sku
        })
