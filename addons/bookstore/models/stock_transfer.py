from odoo import models, fields
from odoo.exceptions import UserError
from ..helper.generate_transfer_line_data import generate_transfer_line_data

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
    _inherit = ['bs.sequence.code']
    _seq_code = 'bs.stock.transfer'
    _rec_name = 'code'

    stocker_id = fields.Many2one('bs.employee')
    sale_id = fields.Many2one('bs.sale.order', ondelete='cascade', readonly=True, string='Sale Order')
    purchase_id = fields.Many2one('bs.purchase.order', ondelete='cascade', readonly=True, string='Purchase Order')
    line_ids = fields.One2many('bs.stock.transfer.line', 'transfer_id')

    date_confirmed = fields.Datetime(readonly=True)
    type = fields.Selection(selection=TRANSFER_TYPES, readonly=True)
    state = fields.Selection(selection=TRANSFER_STATES, default='draft')

    def create_export(self, sale_order):
        line_data = generate_transfer_line_data(sale_order.line_ids)
        return self.create([{
            'sale_id': sale_order.id,
            'type': 'export',
            'line_ids': line_data
        }])

    def create_import(self, purchase_order):
        line_data = generate_transfer_line_data(purchase_order.line_ids)
        return self.create([{
            'purchase_id': purchase_order.id,
            'type': 'import',
            'line_ids': line_data
        }])

    def action_confirm(self):
        for transfer in self:
            transfer.state = 'confirmed'
            transfer.date_confirmed = fields.Datetime.now()
            transfer.line_ids.update_stock_qty()
            if transfer.sale_id:
                transfer.sale_id.state = 'delivered'
            if transfer.purchase_id:
                transfer.purchase_id.state = 'received'

    def unlink(self):
        for transfer in self:
            if transfer.state == 'confirmed':
                raise UserError('Can not delete confirmed transfer!')
        super(StockTransfer, self).unlink()
