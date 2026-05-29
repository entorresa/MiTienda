from odoo import api, models, fields
from ..services.request_api_mitienda import RequestApiMiTienda

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        res = super()._action_done()
        for stock in self:
            print("piking---------1------------------")
            # Conexion con API miTienda
        return res

    def button_validate(self):
        res = super().button_validate()
        for picking in self:
            if picking.state == 'done' and (not picking.sale_id or (picking.sale_id.mitienda_id == 0 and (picking.sale_id.mitienda_code == None or picking.sale_id.mitienda_code == ''))):
                print("ingresando a actulaizar stock--------------")
                conexion = RequestApiMiTienda(self.env)
                for line in picking.move_ids:
                    if line.product_id.mitienda_id != 0 or line.product_id.mitienda_sku != None:
                        #incoming: Se debe incrementar el stock en la API MiTienda.pe solo si existe una conexión mitienda.pe.conexion activa con el valor sync_recepcion == True
                        if picking.picking_type_id.code == 'incoming' and conexion.conexion_id.sync_recepcion:
                            respuesta = conexion.buscar_producto(id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
                            datos={}
                            respuesta = conexion.actualizar_producto(datos=datos, id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
                        #outgoing: Se debe decrementar el stock en la API MiTienda.pe solo si existe una conexión mitienda.pe.conexion activa con el valor sync_entrega == True
                        elif picking.picking_type_id.code == 'outgoing' and conexion.conexion_id.sync_entrega:
                            respuesta = conexion.buscar_producto(id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
                            datos = {}
                            respuesta = conexion.actualizar_producto(datos=datos, id=line.product_id.mitienda_id, sku=line.product_id.mitienda_sku)
            print("piking---------1------------------")
            # Conexion con API miTienda
        return res