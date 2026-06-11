# -*- coding: utf-8 -*-
{
    'name': "API mitienda.pe",
    'summary': "Módulo de sincronización de datos de MiTienda.pe para Odoo",
    'description': """
        Módulo de sincronización de datos de MiTienda.pe para Odoo
    """,
    'author': "DTE S.R.L.",
    'website': "https://www.dte.com.bo",
    'category': 'Sales/Sales',
    'version': '2.0.0',
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        # ----------tablero---------
        'views/tablero.xml',
        # --------------------------
        'views/mitienda_pe_conexion.xml',
        'views/mitienda_pe_partner.xml',
        'views/mitienda_pe_sale_order.xml',
        'views/sale_order.xml',
        'views/product_product.xml',
        'views/mitienda_pe_product.xml',
        # 'views/res_partner.xml',
        'views/product_template.xml',
        'wizards/wizard_mitienda_pe_ventas.xml',
        # ----------accion planificada---------
        'accion_planificada/sincronizar.xml',
        'views/menu.xml',
        ],
    'assets': {
        'web.assets_backend': [
            'api_mitienda_peru/static/src/scss/tablero.scss',
            'api_mitienda_peru/static/src/js/tablero.js',
            'api_mitienda_peru/static/src/xml/tablero_template.xml',
        ],
    },
    'demo': [],
    'license': 'GPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
