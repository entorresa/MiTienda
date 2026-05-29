from odoo import fields
import requests
import logging

_logger = logging.getLogger(__name__)

class RequestApiMiTienda:

    def __init__(self, env, company_id = None):
        self.env = env
        self.company_id = company_id or env.company
        self.conexion_id = self.env['mitienda.pe.conexion'].search([('company_id', '=', self.company_id.id), ('activo', '=', True)], limit=1)
        self.cabecera = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.conexion_id.token}",
        }

    def request_api(self, endpoint, notificacion=False, mensaje='Éxito', operacion='GET', datos={}):
        data = {
            'success': False,
            'error': {
                'code': -1,
                'message': '',
            },
            'data': [],
            'meta': {},
        }
        try:
            if self.conexion_id.token_expiracion < fields.Date.today() or not self.conexion_id:
                data['error']['message'] = 'Token API expirado' if self.conexion_id.token_expiracion < fields.Date.today() else 'No se encontró una conexión activa'
            else:
                if operacion == 'PUT':
                    respuesta = requests.put(self.conexion_id.url + endpoint, headers=self.cabecera,json=datos, timeout=self.conexion_id.timeout_api)
                else:
                    respuesta = requests.get(self.conexion_id.url + endpoint, headers=self.cabecera, timeout=self.conexion_id.timeout_api)
                respuesta.raise_for_status()
                data = respuesta.json()
        except requests.exceptions.HTTPError as e:
            if respuesta.status_code == 404:
                data['error']['message'] = 'Registro inexistente'
            else:
                data['error']['message'] = str(e)
        except Exception as e:
            data['error']['message'] = str(e)
        finally:
            if self.conexion_id.entorno == 'pruebas':
                _logger.info(data)
            if notificacion:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Éxito' if data.get('success') else 'Error',
                        'message': mensaje if data.get('success') else data.get('error', {}).get('message'),
                        'type': 'success' if data.get('success') else 'danger',
                        'sticky': False,
                    },
                }
            else:
                return data

    def probar_conexion(self):
        endpoint = '/mitienda/paymentlinks'
        return self.request_api(endpoint, True, 'Conexión establecida')

    def buscar_venta(self, id=0, code=None):
        if id > 0:
            endpoint = f'/mitienda/order/{id}'
        else:
            endpoint = f'/mitienda/order/code/{code}'
        return self.request_api(endpoint)

    def buscar_ventas(self, fecha_inicio=fields.Date.today(), fecha_fin=fields.Date.today(),  pagina=1):
        fecha_inicio = fields.Date.to_string(fecha_inicio)
        fecha_fin = fields.Date.to_string(fecha_fin)
        endpoint = f'/mitienda/orders?status=1&order=date_created&otype=asc&from={fecha_inicio}&to={fecha_fin}&page={pagina}'
        return self.request_api(endpoint)

    def buscar_producto(self, id=0, sku=None):
        if id > 0:
            endpoint = f'/product/{id}'
        else:
            endpoint = f'/product/sku/{sku}'
        return self.request_api(endpoint)

    def actualizar_producto(self, datos, id=0, sku=None):
        if id > 0:
            endpoint = f'/product/{id}/stock'
        else:
            endpoint = f'/product/sku/{sku}/stock'
        return self.request_api(endpoint, operacion='PUT', datos=datos)
