# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUser(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            tablero = self.env['mitienda.pe.tablero'].search([('user_id', '=', user.id)])
            if not tablero:
                self.env['mitienda.pe.tablero'].create({
                    'user_id': user.id,
                })
        return users
