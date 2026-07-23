# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request
from odoo.modules.module import get_manifest


MANIFEST = get_manifest('api_mitienda_peru')

class ApiMitiendaPeru(http.Controller):
    @http.route('/api/api_mitienda_peru/version', type='http', auth='public', methods=['GET'])
    def index(self, **kw):
        return request.make_response(
            json.dumps({
                'version': MANIFEST.get('version', '-'),
                'status': MANIFEST.get('development_status', '-'),
                'release': MANIFEST.get('release', '-'),
            }),
            headers=[('Content-Type', 'application/json')],
        )