from odoo import api, models, fields
from odoo.exceptions import ValidationError
from ..services.request_api_mitienda import RequestApiMiTienda
from pprint import pp
class WizardMiTiendaPeVentas(models.TransientModel):
    _name = "wizard.mitienda.pe.ventas"
    _description = "wizard sincronización manual de ventas"

    conexion_id = fields.Many2one(string='Conexión', comodel_name="mitienda.pe.conexion")
    fecha_inicio = fields.Date(string="Fecha inicio", required=True, default= fields.Date.today())
    fecha_fin = fields.Date(string="Fecha fin", required=True, default=fields.Date.today())
    url = fields.Char(string='API Host', related='conexion_id.url', readonly=True)
    entorno = fields.Selection(string='Entorno', related='conexion_id.entorno', readonly=True)

    @api.constrains('fecha_inicio', 'fecha_fin')
    def validar(self):
        for record in self:
            if record.fecha_fin and record.fecha_inicio and record.fecha_fin < record.fecha_inicio:
                raise ValidationError("Fecha inicio no debe superar a fecha fin")

    def sincronizar(self):
        # Llamar a buscar_ventas con los parámetros fecha_inicio y fecha_fin
        respuesta = RequestApiMiTienda(self.env).buscar_ventas(fecha_inicio=self.fecha_inicio, fecha_fin=self.fecha_fin)
        ventas_api_codes = []
        pp(respuesta)
        if len(respuesta['data']) > 0:
            for data in respuesta['data']:
                # Buscar ventas sale.order
                obj_venta = self.env['sale.order'].search([('mitienda_code', '=', data['code'])])
                if not obj_venta:
                    ventas_api_codes += data['code']
        # Para cada code llamar a buscar_venta pasando el parámetro code
        if len(ventas_api_codes) > 0:
            for venta_code in ventas_api_codes:
                respuesta = RequestApiMiTienda(self.env).buscar_venta(code=venta_code)
                if respuesta['success'] == True:
                    # verificar si existe cliente
                    obj_cliente = self.buscar_cliente(id=respuesta['data']['customer']['id'], email=respuesta['data']['billing_info']['email'], doc_number=respuesta['data']['billing_info']['doc_number'])
                    if not obj_cliente:
                        # registra nuevo cliente
                        obj_cliente = self.env['res.partner'].create({
                            'name': f"{respuesta['data']['billing_info']['name']} {respuesta['data']['billing_info']['last_name']}",
                            'email': respuesta['data']['billing_info']['email'],
                            'vat': respuesta['data']['billing_info']['doc_number'],
                            'mitienda_id': respuesta['data']['customer']['id'],
                            'mitienda_email': respuesta['data']['billing_info']['email'],
                            'mitienda_doc_number': respuesta['data']['billing_info']['doc_number'],
                        })
                        # registra en bitacora de clientes
                        obj_cliente_bitacora = self.env['mitienda.pe.partner'].create({
                            'conexion_id': self.conexion_id.id,
                            'fecha_sincronizacion': fields.Datetime.now,
                            'company_id': self.env.company.id,
                            'partner_id': obj_cliente.id,
                            'mitienda_name': respuesta['data']['billing_info']['name'],
                            'mitienda_last_name': respuesta['data']['billing_info']['last_name'],
                            'mitienda_email': respuesta['data']['billing_info']['email'],
                            'mitienda_doc_number': respuesta['data']['billing_info']['doc_number'],
                        })
                    for item in respuesta['data']['items']:
                        obj_producto = self.buscar_producto(id=item['id'], sku=item['sku'])
                        if not obj_producto:
                            # registrar producto
        return False

    def buscar_cliente(self, id, email, doc_number):
        obj_cliente = self.env['res.partner'].search(['|','|',('mitienda_id', '=', id), ('mitienda_email', '=', email), ('mitienda_doc_number','=', doc_number)])
        return obj_cliente

    def buscar_producto(self, id, sku):
        obj_producto = self.env['product.product'].search(['|', ('mitienda_id', '=', id), ('mitienda_sku', '=', sku)])
        return obj_producto

    @api.onchange('conexion_id')
    def conexion_onchange(self):
        if not self.conexion_id:
            return {
                'warning':{
                    'title': 'Error',
                    'message': 'Debe establecer una conexión activa para la compañía actual',
                }
            }

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        conexion = RequestApiMiTienda(self.env)
        if conexion.conexion_id:
            res['conexion_id'] = conexion.conexion_id.id
        return res