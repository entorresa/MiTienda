from odoo import fields, Command
import logging
from .request_api_mitienda import RequestApiMiTienda
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class SyncAPIMiTienda:
    def __init__(self, env):
        self.env = env
        conexion = RequestApiMiTienda(self.env)
        self.conexion_id = conexion.conexion_id

    def sincronizar_ventas(self, fecha_inicio=fields.Date.today(), fecha_fin=fields.Date.today(), headless=False):
        # Llamar a buscar_ventas con los parámetros fecha_inicio y fecha_fin
        error = False
        mensaje = ''
        contador_total = 0
        contador_exito = 0
        contador_error = 0
        if not self.conexion_id:
            raise Exception('Debe establecer una conexión activa para la compañía actual')
        try:
            mensaje = "Sincronización automática de ventas iniciada" if headless else "Sincronización de ventas iniciada"
            self.registrar_bitacora_venta(mensaje=mensaje, sync_venta_logica=False)
            estado = True
            pagina = 1
            ventas_api_codes = []
            conteo_requests = 0
            while estado:
                respuesta = RequestApiMiTienda(self.env).buscar_ventas(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, pagina=pagina)
                conteo_requests += 1
                estado = respuesta.get('success', False)
                if not estado:
                    raise Exception(respuesta.get('error', {}).get('message', 'Error'))
                if len(respuesta['data']) > 0:
                    for data in respuesta['data']:
                        # Buscar ventas sale.order
                        obj_venta = self.env['sale.order'].search([('mitienda_code', '=', data['code'])])
                        if not obj_venta:
                            ventas_api_codes.append(data['code'])
                if not respuesta['pagination']['next'] or len(respuesta['data']) == 0 or respuesta['pagination']['total'] == 0:
                    estado = False
                pagina += 1
            # -------------------------------
            conteo_requests += len(ventas_api_codes)
            if conteo_requests > 100:
                raise Exception(f'Límite de número de consultas excedido: {len(conteo_requests)}')
            # Para cada code llamar a buscar_venta pasando el parámetro code
            if len(ventas_api_codes) > 0 and len(ventas_api_codes) <= 90:
                for venta_code in ventas_api_codes:
                    respuesta = RequestApiMiTienda(self.env).buscar_venta(code=venta_code)
                    if respuesta['success'] is True and 'id' in respuesta['data'] and 'code' in respuesta['data'] and 'billing_info' in respuesta['data'] and 'customer' in respuesta['data'] and 'items' in respuesta['data']:
                        # Solo ventas con estado Aprobado (1)
                        if respuesta['data']['status'] == 1 and len(respuesta['data']['items']) > 0:
                            contador_total += 1
                            # verificar si existe cliente
                            obj_bitacora_cliente = self.env['mitienda.pe.partner'].search([
                                '|',
                                ('mitienda_doc_number', '=', respuesta['data']['billing_info']['doc_number']),
                                ('mitienda_email', '=', respuesta['data']['billing_info']['email']),
                            ], limit=1, order="id desc")
                            if self.conexion_id.sync_cliente_logica == 'cliente_predefinido':
                                obj_cliente = self.conexion_id.sync_cliente_predefinido
                            else:
                                if obj_bitacora_cliente:
                                    obj_cliente = obj_bitacora_cliente.partner_id
                                else:
                                    obj_cliente = self.buscar_cliente(id=respuesta['data']['customer'].get('id'), email=respuesta['data']['billing_info']['email'], doc_number=respuesta['data']['billing_info']['doc_number'])
                                    if not obj_cliente:
                                        # registra nuevo cliente
                                        obj_cliente = self.env['res.partner'].create({
                                            'name': f"{respuesta['data']['billing_info']['name']} {respuesta['data']['billing_info']['last_name']}",
                                            'email': respuesta['data']['billing_info']['email'],
                                            'vat': respuesta['data']['billing_info']['doc_number'],
                                            'mitienda_id': respuesta['data']['customer'].get('id'),
                                            'mitienda_email': respuesta['data']['billing_info']['email'],
                                            'mitienda_doc_number': respuesta['data']['billing_info']['doc_number'],
                                        })
                                        # registra en bitacora de clientes
                                        obj_bitacora_cliente = self.registrar_bitacora_cliente(respuesta['data']['billing_info'], obj_cliente)
                                    else:
                                        if not obj_cliente.email or not obj_cliente.vat or not obj_cliente.mitienda_id or not obj_cliente.mitienda_email or not obj_cliente.mitienda_doc_number:
                                            obj_cliente.write({
                                                'email': respuesta['data']['billing_info']['email'],
                                                'vat': respuesta['data']['billing_info']['doc_number'],
                                                'mitienda_id': respuesta['data']['customer'].get('id'),
                                                'mitienda_email': respuesta['data']['billing_info']['email'],
                                                'mitienda_doc_number': respuesta['data']['billing_info']['doc_number'],
                                            })

                            # Buscar productos de Odoo por SKU
                            skus_inexistentes = []
                            productos = []
                            for item in respuesta['data']['items']:
                                obj_producto = self.buscar_producto(id=item['id'], sku=item['sku'])
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
                                self.registrar_bitacora_venta(
                                    fecha_venta=respuesta['data']['date_created'],
                                    mensaje=f"No se pudo sincronizar la venta debido a la inexistencia de SKU: {', '.join(skus_inexistentes)}",
                                    partner_id=obj_cliente.id,
                                    error=True,
                                    mitienda_order_code=respuesta['data']['code'],
                                    mitienda_order_id=respuesta['data']['id'],
                                    status=respuesta['data']['status'],
                                    mitienda_partner_id=obj_bitacora_cliente.id,
                                )
                                contador_error += 1
                            else:
                                billing_info = respuesta.get('data', {}).get('billing_info', {}).get('e-billing', {})
                                pdf = billing_info.get('url_pdf', None)
                                serie = billing_info.get('serie', None)
                                correlative = billing_info.get('correlative', None)
                                obj_venta = self.buscar_venta(
                                    id=respuesta['data']['id'],
                                    code=respuesta['data']['code'],
                                    cliente_id=obj_cliente.id,
                                    productos=productos,
                                    pdf=pdf,
                                    serie=serie,
                                    correlative=correlative,
                                )
                                if obj_venta:
                                    # Registrar bitacora de ventas
                                    self.registrar_bitacora_venta(
                                        fecha_venta=respuesta['data']['date_created'],
                                        mensaje=f"Venta sincronizada: {respuesta['data']['code']}",
                                        sale_order_id=obj_venta.id,
                                        partner_id=obj_venta.partner_id.id,
                                        mitienda_order_code=respuesta['data']['code'],
                                        mitienda_order_id=respuesta['data']['id'],
                                        status=respuesta['data']['status'],
                                        mitienda_partner_id=obj_bitacora_cliente.id,
                                        pdf=pdf
                                    )
                                    contador_exito += 1
                                else:
                                    self.registrar_bitacora_venta(
                                        fecha_venta=respuesta['data']['date_created'],
                                        mensaje=f"No se pudo sincronizar la venta debido a error de base de datos",
                                        partner_id=obj_cliente.id,
                                        error=True,
                                        mitienda_order_code=respuesta['data']['code'],
                                        mitienda_order_id=respuesta['data']['id'],
                                        status=respuesta['data']['status'],
                                        mitienda_partner_id=obj_bitacora_cliente.id,
                                    )
                                    contador_error += 1
                    else:
                        self.registrar_bitacora_venta(mensaje=respuesta['error']['message'], error=True)
                        contador_error += 1
                mensaje = f"{contador_exito} ventas registradas - {contador_error} errores - {contador_total} ventas en total"
        except Exception as e:
            error = True
            mensaje = str(e)
            self.registrar_bitacora_venta(
                mensaje=mensaje,
                error=True,
            )
        finally:
            mensaje = "Sincronización automática de ventas finalizada" if headless else "Sincronización de ventas finalizada"
            self.registrar_bitacora_venta(mensaje=mensaje, sync_venta_logica=False)
            if not headless:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error' if error else 'Éxito',
                        'message': mensaje,
                        'type': 'danger' if (error and contador_error == 0) else ('warning' if contador_error > 0 else 'success'),
                        'sticky': False,
                        'next': {
                            'type': 'ir.actions.client',
                            'tag': 'soft_reload',
                        },
                    },
                }

    def buscar_cliente(self, id, email, doc_number):
        domain = []
        operador = []
        if id:
            domain.append(('mitienda_id', '=', id))
        if email:
            domain.append(('mitienda_email', '=', email))
        if doc_number:
            domain.append(('mitienda_doc_number', '=', doc_number))
        if len(domain) == 3:
            operador.extend(['|', '|'])
        elif len(domain) == 2:
            operador.append('|')
        domain = operador+domain
        obj_cliente = self.env['res.partner'].search(domain, limit=1, order='id asc')
        return obj_cliente

    def buscar_producto(self, id, sku):
        domain = []
        operador = []
        if id:
            domain.append(('mitienda_id', '=', id))
        if sku:
            domain.append(('mitienda_sku', '=', sku))
        if len(domain) == 2:
            operador.append('|')
        domain = operador+domain
        obj_producto = self.env['product.product'].search(domain, limit=1, order='id asc')
        if obj_producto and not obj_producto.mitienda_id or obj_producto.mitienda_id == 0:
            obj_producto.write({
                'mitienda_id': id,
            })
        return obj_producto

    def buscar_venta(self, id, code, cliente_id, productos, pdf=None, serie=None, correlative=None):
        domain = []
        operador = []
        if id:
            domain.append(('mitienda_id', '=', id))
        if code:
            domain.append(('mitienda_code', '=', code))
        if len(domain) == 2:
            operador.append('|')
        domain = operador+domain
        obj_venta = self.env['sale.order'].search(domain, limit=1, order='id asc')
        if not obj_venta:
            try:
                # cotizacion
                obj_venta = self.env['sale.order'].create({
                    'partner_id': cliente_id,
                    'mitienda_id': id,
                    'mitienda_code': code,
                    'mitienda_sunat_pdf': pdf,
                    'mitienda_serie': serie,
                    'mitienda_correlative': correlative,
                    'order_line': [Command.create(linea) for linea in productos],
                })
            except Exception as e:
                _logger.error(str(e))
                _logger.error('Error al registrar la venta: ' + code)
        if obj_venta:
            if self.conexion_id.sync_venta_logica == 'venta':
                # venta confirmado
                obj_venta.action_confirm()
            elif self.conexion_id.sync_venta_logica == 'factura_borrador' or self.conexion_id.sync_venta_logica == 'factura_publicada':
                # venta confirmado y crea la factura en borrador
                try:
                    obj_venta.action_confirm()
                except Exception as e:
                    _logger.error(str(e))
                    _logger.error('Error al confirmar venta: ' + obj_venta.name)
                try:
                    factura = obj_venta._create_invoices()
                except Exception as e:
                    _logger.error(str(e))
                    _logger.error('Error al registrar factura asociada a la venta: ' + obj_venta.name)
                if self.conexion_id.sync_venta_logica == 'factura_publicada' and factura:
                    try:
                        factura.action_post()
                    except Exception as e:
                        _logger.error(str(e))
                        _logger.error('Error al publicar factura asociada a la venta: ' + factura.name)
            # por else no hace nada, la venta se queda como cotizacion
        return obj_venta

    def registrar_bitacora_cliente(self, respuesta, obj_cliente):
        obj_bitacora_cliente = self.env['mitienda.pe.partner'].create({
            'conexion_id': self.conexion_id.id,
            'fecha_sincronizacion': fields.Datetime.now(),
            'company_id': self.env.company.id,
            'partner_id': obj_cliente.id,
            'mitienda_name': respuesta['name'],
            'mitienda_last_name': respuesta['last_name'],
            'mitienda_email': respuesta['email'],
            'mitienda_doc_number': respuesta['doc_number'],
        })
        return obj_bitacora_cliente

    def registrar_bitacora_venta(self, fecha_venta=None, mensaje=None, sale_order_id=None, partner_id=None, error=False, mitienda_order_code=None, mitienda_order_id=None, status=None, pdf=None, mitienda_partner_id=None, sync_venta_logica=True):
        self.env['mitienda.pe.sale.order'].create({
            'conexion_id': self.conexion_id.id,
            'fecha_sincronizacion': fields.Datetime.now(),
            'fecha_venta': fecha_venta,
            'mensaje': mensaje,
            'sale_order_id': sale_order_id,
            'partner_id': partner_id,
            'error': error,
            'company_id': self.env.company.id,
            'sync_cliente_logica': self.conexion_id.sync_cliente_logica,
            'sync_cliente_predefinido': self.conexion_id.sync_cliente_predefinido.id if self.conexion_id.sync_cliente_logica == 'cliente_predefinido' else None,
            'sync_venta_logica': self.conexion_id.sync_venta_logica if sync_venta_logica else None,
            'mitienda_order_code': mitienda_order_code,
            'mitienda_order_id': mitienda_order_id,
            'mitienda_order_status': str(status) if status else status,
            'mitienda_sunat_pdf': pdf,
            'mitienda_partner_id': mitienda_partner_id,
        })
