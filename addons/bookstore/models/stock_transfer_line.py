from odoo import models, fields, api
from odoo.exceptions import UserError
from .stock_transfer import TRANSFER_STATES, TRANSFER_TYPES


class StockTransferLine(models.Model):
    _name = 'bs.stock.transfer.line'
    _rec_name = 'book_id'
    _sql_constraints = [
        ('unique_book', 'unique(transfer_id, book_id)', 'Duplicated books!'),
        ('qty_greater_zero', 'CHECK (qty > 0)', 'Error: Qty must greater than 0!')
    ]

    book_id = fields.Many2one('bs.book')
    transfer_id = fields.Many2one('bs.stock.transfer', ondelete='cascade')

    qty = fields.Integer(default=1)
    stock_qty = fields.Integer(related='book_id.stock_qty')
    forecasted_stock_qty = fields.Integer(compute='_compute_forecasted_qty')
    origin_stock_qty = fields.Integer(readonly=True)
    modified_stock_qty = fields.Integer(readonly=True)
    final_stock_qty = fields.Integer(readonly=True)

    state = fields.Selection(selection=TRANSFER_STATES, related='transfer_id.state')
    date_confirmed = fields.Datetime(related='transfer_id.date_confirmed')
    type = fields.Selection(selection=TRANSFER_TYPES, related='transfer_id.type')

    def update_stock_qty(self):
        for line in self:
            new_qty = line.forecasted_stock_qty
            old_qty = line.book_id.stock_qty
            if new_qty < 0:
                raise UserError(f'{line.book_id.name} not have enough stock!')
            line.origin_stock_qty = old_qty
            line.book_id.stock_qty = new_qty
            line.final_stock_qty = new_qty
            line.modified_stock_qty = new_qty - old_qty

    @api.depends('book_id.stock_qty', 'transfer_id.type', 'qty')
    def _compute_forecasted_qty(self):
        for line in self:
            current_stock = line.book_id.stock_qty
            ratio = 1 if line.transfer_id.type == 'import' else -1
            line.forecasted_stock_qty = current_stock + ratio * line.qty
