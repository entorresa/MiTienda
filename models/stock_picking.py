from odoo import api, models, fields
from ..services.request_api_mitienda import RequestApiMiTienda

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        for picking in self:
            print("picking.state:", picking.state, "SALE:", picking.sale_id, "idventa:", picking.sale_id.mitienda_id, "code venta:",picking.sale_id.mitienda_code)
            if picking.state == 'done' and (not picking.sale_id or (picking.sale_id.mitienda_id == 0 and not picking.sale_id.mitienda_code)):
                print("ingresando a actulaizar stock--------------")
                conexion = RequestApiMiTienda(picking.env)
                for line in picking.move_ids:
                    if line.product_id.mitienda_id != 0 or line.product_id.mitienda_sku != None:
                        if (picking.picking_type_id.code == 'incoming' and conexion.conexion_id.sync_recepcion) or (picking.picking_type_id.code == 'outgoing' and conexion.conexion_id.sync_entrega):
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
                                    print(f"Restaurando stock a: {stock_inicial}")
                                    respuesta2 = conexion.actualizar_producto(datos=datos, id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
                                    if respuesta2['success'] is True:
                                        self.registrar_bitacora_producto(conexion.conexion_id.id,
                                                                            product_temp_id = line.product_id.product_tmpl_id.id,
                                                                            product_product_id = line.product_id.id,
                                                                            picking_id = picking.id,
                                                                            stock_inicial = stock,
                                                                            stock_ajuste = stock_ajuste_prueba,
                                                                            mitienda_id = respuesta['data']['id'],
                                                                            mitienda_sku = respuesta['data']['sku'])
        return res

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
