# -*- coding: utf-8 -*-
{
    'name': "API mitienda.pe",
    'summary': "Módulo para sincronizar datos entre Odoo y la API mitienda.pe",
    'description': """
        Módulo para sincronizar datos entre Odoo y la API mitienda.pe
    """,
    'author': "DTE S.R.L.",
    'website': "https://www.dte.com.bo",
    'category': 'Sales/Sales',
    'version': '0.0.1',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/mitienda_pe_conexion.xml',
        'views/mitienda_pe_partner.xml',
        'views/mitienda_pe_sale_order.xml',
        'views/menu.xml',
        ],
    'demo': [],
    'license': 'GPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
