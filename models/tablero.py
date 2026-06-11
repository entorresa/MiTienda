from odoo import models, fields, api
from datetime import datetime, timedelta

class Tablero(models.Model):
    _name = 'api_mitienda_peru.tablero'
    _description = 'Tablero'

    user_id = fields.Many2one('res.users', string='Usuario')
    is_favorite = fields.Boolean(string='Favorito', default=False)
    color = fields.Integer(string='Color', default=0)
    
    _sql_constraints = [
        ('user_unique', 'unique(user_id)',
        'Ya existe una preferencia para este usuario')
    ]

    @api.model
    def get_sync_data(self):
        hoy = datetime.now().date()
        hace_7_dias = hoy - timedelta(days=7)
        ventas = self.env['mitienda.pe.sale.order'].search([
            ('error', '=', False),
            ('sale_order_id','!=',False),
            ('mitienda_order_id','>',0),
            ('mitienda_order_code','!=',''),
            ('mitienda_order_status','=','1'),
            ('fecha_sincronizacion','>=', hace_7_dias.strftime('%d/%m/%Y')),
        ])
        conteo_por_dia = {}
        for i in range(7):
            dia = hoy - timedelta(days=i)
            conteo_por_dia[dia.strftime('%d/%m/%Y')] = 0
        
        for venta in ventas:
            dia = venta.fecha_sincronizacion.strftime('%d/%m/%Y')
            if dia in conteo_por_dia:
                conteo_por_dia[dia] += 1

        fechas = sorted(conteo_por_dia.keys())
        return {
            'labels': fechas,
            'data': [conteo_por_dia[f] for f in fechas],
        }
    @api.model
    def get_ultimas_sincronizaciones(self):
        ventas = self.env['mitienda.pe.sale.order'].search([
            ('error', '=', False),
            ('sale_order_id','!=',False),
            ('mitienda_order_id','>',0),
            ('mitienda_order_code','!=',''),
            ('mitienda_order_status','=','1'),
        ], limit=3, order='fecha_sincronizacion desc')

        return[{
            'id': v.id,
            'nombre': str(v.fecha_sincronizacion),
            'sale_order_id': v.sale_order_id.id if v.sale_order_id else False,
            'sale_order_name': v.sale_order_id.name if v.sale_order_id else '',
            'fecha':v.fecha_sincronizacion.strftime('%d/%m/%Y') if v.fecha_sincronizacion else '',
        } for v in ventas]

    @api.model
    def set_favorite(self, is_favorite):
        registro = self.search([('user_id','=',self.env.uid)], limit=1)
        if registro:
            registro.write({'is_favorite': is_favorite})
        else:
            self.create({
                'user_id': self.env.uid,
                'is_favorite': is_favorite,
            })

    @api.model
    def set_color(self, color):
        registro = self.search([('user_id','=',self.env.uid)], limit=1)
        if registro:
            registro.write({'color': color})
        else:
            self.create({
                'user_id': self.env.uid,
                'color': color,
            })

    @api.model
    def get_preferencias(self):
        registro = self.search([('user_id','=',self.env.uid)], limit=1)
        if registro:
            return{
                'is_favorite': registro.is_favorite,
                'color': registro.color,
            }
        return {'is_favorite': False, 'color':0}