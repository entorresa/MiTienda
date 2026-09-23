from odoo import http, Command
from odoo.http import request
import json
from ..services.sync_api_mitienda import SyncAPIMiTienda

class MiTiendaSaleOrderController(http.Controller):

    #@http.route('/webhook/sale_order', type='http', auth='bearer', csrf=False, methods=['POST'])
    @http.route('/webhook/sale_order', type='http', auth='public', csrf=False, methods=['POST'])
    def webhook_sale_order(self, **kwargs):
        try:
            body = json.loads(request.httprequest.data.decode('utf-8'))
            if body['object'] != 'order' or body['status'] != 1:
                raise Exception('El estado de la venta debe ser igual a 1')
            conexion_ids = request.env["mitienda.pe.conexion"].sudo().search([('activo', '=', True)])
            user = request.env.ref('base.user_root') # super usuario
            if not user or not conexion_ids:
                return request.make_json_response(
                    {
                        'success': False,
                        'message': 'No se encontró una configuración activa'
                    },
                    status=404,
                )
            if not ('id' in body and 'code' in body and 'billing_info' in body and 'customer' in body and 'items' in body):
                return request.make_json_response(
                    {
                        'success': False,
                        'message': 'Estructura de datos inválida'
                    },
                    status=422,
                )
            if len(body['items']) == 0:
                return request.make_json_response(
                    {
                        'success': False,
                        'message': 'Solo se pueden registrar ventas con uno mas items'
                    },
                    status=422,
                )
            for conexion_id in conexion_ids:
                # establecer usuario a ENV, para facilitar consultas sin autenticacion y para no usar sudo()
                # usar env para consultas y llamadas a metodo externos de controller
                env = request.env(user=user.id)
                env.company = conexion_id.company_id
                obj_venta = env['sale.order'].with_user(user).with_company(conexion_id.company_id).search([('mitienda_id', '=', body['id'])])
                if not obj_venta:
                    sincronizacion = SyncAPIMiTienda(env)
                    # buscar cliente
                    obj_cliente = sincronizacion.buscar_cliente(id=body['customer'].get('id'), email=body['billing_info']['email'], doc_number=body['billing_info']['doc_number'])
                    obj_bitacora_cliente = env['mitienda.pe.partner'].with_user(user).with_company(conexion_id.company_id).search([
                        '|',
                        ('mitienda_doc_number', '=', body['billing_info']['doc_number']),
                        ('mitienda_email', '=', body['billing_info']['email']),
                    ], limit=1, order="id desc")
                    if not obj_cliente:
                        # registra nuevo cliente
                        obj_cliente = env['res.partner'].with_user(user).with_company(conexion_id.company_id).create({
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
                        if not obj_producto or item['quantity'] <= 0 or item['unit_price'] < 0:
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
                        sincronizacion.registrar_bitacora_venta(
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
                        pdf, serie, correlative = sincronizacion.extraer_datos_sunat(body)
                        obj_venta = sincronizacion.buscar_venta(id=body['id'], code=body['code'], cliente_id=obj_cliente.id, productos=productos, pdf=pdf, serie=serie, correlative=correlative, fecha_venta=body.get('date_created'), fecha_pago=body.get('date_payment'))
                        if obj_venta:
                            # Registrar bitacora de ventas
                            sincronizacion.registrar_bitacora_venta(
                                fecha_venta = body['date_created'],
                                mensaje = f"Sincronización de venta mediante webhook: {body['code']}",
                                sale_order_id = obj_venta.id,
                                partner_id = obj_venta.partner_id.id,
                                mitienda_order_code = body['code'],
                                mitienda_order_id = body['id'],
                                status = body['status'],
                                mitienda_partner_id=obj_bitacora_cliente.id,
                            )
            return request.make_json_response(
                {
                    'success': True,
                    'message':'Venta sincronizada'
                },
                status=200,
            )
        except Exception as e:
            return request.make_json_response(
                {
                    'success': False,
                    'message': str(e)
                },
                status=500,
            )
