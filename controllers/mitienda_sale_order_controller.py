from odoo import http, Command
from odoo.http import request
from ..services.sync_api_mitienda import SyncAPIMiTienda

class MiTiendaSaleOrderController(http.Controller):

    @http.route('/webhook/sale_order', type='json', auth='public', csrf=False, methods=['POST'])
    def webhook_sale_order(self, **kwargs):
        body = request.jsonrequest
        print("data----------", body)
        if body['object'] == 'order' and body['status'] == 1:
            obj_venta = self.env['sale.order'].search([('mitienda_id', '=', body['id'])])
            if not obj_venta:
                sincronizacion = SyncAPIMiTienda(self.env)
                # buscar cliente
                obj_cliente = sincronizacion.buscar_cliente(id=body['customer'].get('id'), email=body['billing_info']['email'], doc_number=body['billing_info']['doc_number'])
                print("cliente encontrado ...:", obj_cliente, obj_cliente.name)
                if not obj_cliente:
                    # registra nuevo cliente
                    obj_cliente = self.env['res.partner'].create({
                        'name': f"{body['billing_info']['name']} {body['billing_info']['last_name']}",
                        'email': body['billing_info']['email'],
                        'vat': body['billing_info']['doc_number'],
                        'mitienda_id': body['customer'].get('id'),
                        'mitienda_email': body['billing_info']['email'],
                        'mitienda_doc_number': body['billing_info']['doc_number'],
                    })
                    # registra en bitacora de clientes
                    obj_bitacora_cliente = sincronizacion.registrar_bitacora_cliente(body['billing_info'], obj_cliente)
                # Buscar productos de Odoo por SKU
                skus_inexistentes = []
                productos = []
                for item in body['items']:
                    obj_producto = sincronizacion.buscar_producto(id=item['id'], sku=item['sku'])
                    if not obj_producto:
                        skus_inexistentes.append(item['sku'])
                    else:
                        productos.append({
                            'product_id': obj_producto.id,
                            'product_uom_qty': item['quantity'],
                            'tax_id': [Command.clear()],
                            'discount': 0,
                            'price_unit': item['unit_price'],
                        })
                        # registrar bitacora
                if len(skus_inexistentes) > 0:
                    self.registrar_bitacora_venta(
                        fecha_venta = body['date_created'],
                        mensaje = f"No se pudo sincronizar la venta debido a la inexistencia de SKU: {', '.join(skus_inexistentes)}",
                        partner_id = obj_cliente.id,
                        error = True,
                        mitienda_order_code = body['code'],
                        mitienda_order_id = body['id'],
                        status = body['status'],
                        mitienda_partner_id = obj_bitacora_cliente.id,
                    )
                else:
                    #venta = sincronizacion.buscar_venta(self, id, code, cliente_id, productos)
