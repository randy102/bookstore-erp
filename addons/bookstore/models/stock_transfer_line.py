from odoo import models, fields, api
from odoo.exceptions import UserError


class StockTransferLine(models.Model):
    _name = 'bs.stock.transfer.line'
    _rec_name = 'book_id'
    _sql_constraints = [('unique_book', 'unique(transfer_id, book_id)', 'Duplicated books!')]

    book_id = fields.Many2one('bs.book')
    transfer_id = fields.Many2one('bs.stock.transfer', ondelete='cascade')
    qty = fields.Integer(default=1)
    stock_qty = fields.Integer(related='book_id.stock_qty')
    forecasted_stock_qty = fields.Integer(compute='_compute_forecasted_qty')

    def update_stock_qty(self):
        for line in self:
            new_qty = line.forecasted_stock_qty
            if new_qty < 0:
                raise UserError(f'{line.book_id.name} not have enough stock!')
            line.book_id.stock_qty = new_qty

    @api.depends('book_id.stock_qty', 'transfer_id.type', 'qty')
    def _compute_forecasted_qty(self):
        for line in self:
            current_stock = line.book_id.stock_qty
            ratio = 1 if line.transfer_id.type == 'import' else -1
            line.forecasted_stock_qty = current_stock + ratio * line.qty
