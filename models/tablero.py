from odoo import models, fields, api, _
from datetime import datetime, timedelta

class Tablero(models.Model):
    _name = 'mitienda.pe.tablero'
    _description = 'Tablero'

    user_id = fields.Many2one('res.users', string='Usuario', ondelete="cascade", default=lambda self: self.env.user)
    name = fields.Char(string='Nombre tablero', size=128, default='Sincronizaciones de ventas')
    is_favorite = fields.Boolean(string='Favorito', default=True)
    color = fields.Integer(string='Color', default=0)
    
    sincronizaciones_count = fields.Integer(string='Cantidad de sincronizaciones',compute='_compute_sincronizaciones_count')
    ultimas_sincronizaciones_html = fields.Html(string='Ultimas sincronizaciones',compute='_compute_ultimas_sincronizaciones_html',sanitize=False)
    grafico_data = fields.Char(string='Datos del grafico',compute='_compute_grafico_data')

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
                fecha = venta.fecha_sincronizacion.strftime('%d/%m/%Y') if venta.fecha_sincronizacion else '-'
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

    @api.model
    def _user_tablero_seeder(self):
        users = self.env['res.users'].search([])
        for user in users:
            tablero = self.env['mitienda.pe.tablero'].sudo().search([('user_id', '=', user.id)])
            if not tablero:
                self.env['mitienda.pe.tablero'].create({
                    'user_id': user.id,
                })
