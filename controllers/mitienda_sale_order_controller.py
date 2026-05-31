from odoo import http
from odoo.http import request


class MiTiendaSaleOrderController(http.Controller):

    @http.route('/webhook/sale_order', type='http', auth='public', csrf=False, methods=['POST'])
    def webhook_sale_order(self):
