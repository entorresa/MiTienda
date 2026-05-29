from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        res = super()._action_done()
        for stock in self:
            # Conexion con API miTienda
        return res
