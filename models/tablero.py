from odoo import models, fields, api, _
from datetime import datetime, timedelta

class Tablero(models.Model):
    _name = 'mitienda.pe.tablero'
    _description = 'Tablero'

    user_id = fields.Many2one('res.users', string='Usuario')
    name = fields.Char(string='Nombre tablero', size=128, default='Tablero')
    is_favorite = fields.Boolean(string='Favorito', default=False)
    color = fields.Integer(string='Color', default=0)
    
    sincronizaciones_count = fields.Integer(string='Cantidad de sincronizaciones',compute='_compute_sincronizaciones_count')
    ultimas_sincronizaciones_html = fields.Html(string='Ultimas sincronizaciones',compute='_compute_ultimas_sincronizaciones_html',sanitize=False)
    grafico_data = fields.Char(string='Datos del grafico',compute='_compute_grafico_data')

    # _sql_constraints = [
    #     ('user_unique', 'unique(user_id)',
    #     'Ya existe una preferencia para este usuario')
    # ]

    def _get_ventas_domain(self):
        return [
            ('error','=',False),
            ('sale_order_id','!=',False),
            ('mitienda_order_id','>',0),
            ('mitienda_order_code','!=',False),
            ('mitienda_order_status','in',['1',1]),
        ]
        
    @api.depends('name')
    def _compute_sincronizaciones_count(self):
        Venta = self.env['mitienda.pe.sale.order']
        total = Venta.search_count(self._get_ventas_domain())
        for rec in self:
            rec.sincronizaciones_count = total

    @api.depends('name')
    def _compute_ultimas_sincronizaciones_html(self):
        Venta=self.env['mitienda.pe.sale.order']
        ultimas=Venta.search(self._get_ventas_domain(), order='fecha_sincronizacion desc', limit=3)

        for rec in self:
            if not ultimas:
                rec.ultimas_sincronizaciones_html=''
                continue

            filas=[]
            for venta in ultimas:
                nombre = venta.sale_order_id.name if venta.sale_order_id else (venta.mitienda_order_code or '-') 
                sale_id = venta.sale_order_id.id if venta.sale_order_id else 0
                fecha = venta.fecha_sincronizacion.strftime('%d/%m/%Y %H:%M') if venta.fecha_sincronizacion else '-'
                filas.append(f'''
                    <div class="row">
                        <div class="col overflow-hidden text-start">
                            <a href="#" class="o_siat_pv_name" data-sale-id="{sale_id}">
                                {nombre}
                            </a>
                        </div>
                        <div class="col-auto text-end text-muted small">{fecha}</div>
                    </div>
                ''')

            rec.ultimas_sincronizaciones_html = f'''
                <div class="o_mitienda_ultimas_title">Últimas Sincronizaciones</div>
                {''.join(filas)}
            '''
    
    @api.depends('name')
    def _compute_grafico_data(self):
        hoy = datetime.now().date()
        hace_7_dias = hoy-timedelta(days=7)
        ventas = self.env['mitienda.pe.sale.order'].search(
            self._get_ventas_domain() + [('fecha_sincronizacion','>=',hace_7_dias.strftime('%Y-%m-%d'))]
        )
        conteo_por_dia={}
        for i in range(7):
            dia=hoy-timedelta(days=i)
            conteo_por_dia[dia.strftime('%d/%m/%Y')]=0

        for venta in ventas:
            if venta.fecha_sincronizacion:
                dia=venta.fecha_sincronizacion.strftime('%d/%m/%Y')
                if dia in conteo_por_dia:
                    conteo_por_dia[dia] += 1

        fechas = sorted(conteo_por_dia.keys(), key=lambda d: datetime.strptime(d, '%d/%m/%Y'))
        import json
        for rec in self:
            rec.grafico_data = json.dumps({
                'labels':fechas,
                'data':[conteo_por_dia[f] for f in fechas],
            })
        
    def action_toggle_favorite(self):
        for rec in self:
            rec.is_favorite = not rec.is_favorite

    def action_ver_mas(self):
        return{
            'type':'ir.actions.act_window',
            'name':_('Sincronizaciones de ventas'),
            'res_model':'mitienda.pe.sale.order',
            'view_mode':'list,form',
            'target':'current',
        }

    
    
'''
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
        
'''