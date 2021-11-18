from odoo import models, fields
from odoo.exceptions import UserError

TRANSFER_TYPES = [
    ('import', 'Import'),
    ('export', 'Export')
]

TRANSFER_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed')
]


class StockTransfer(models.Model):
    _name = 'bs.stock.transfer'
    _inherit = ['bs.sequence.name']
    _seq_code = 'bs.stock.transfer'

    stocker_id = fields.Many2one('bs.employee')
    sale_id = fields.Many2one('bs.sale.order')
    line_ids = fields.One2many('bs.stock.transfer.line', 'transfer_id')

    date_confirmed = fields.Datetime(readonly=True)
    type = fields.Selection(selection=TRANSFER_TYPES, default='import')
    state = fields.Selection(selection=TRANSFER_STATES, default='draft')

    def action_confirm(self):
        for transfer in self:
            transfer.state = 'confirmed'
            transfer.date_confirmed = fields.Datetime.now()
            transfer.line_ids.update_stock_qty()

    def unlink(self):
        for transfer in self:
            if transfer.state == 'confirmed':
                raise UserError('Can not delete confirmed transfer!')
