from odoo import models, fields, api


class Author(models.Model):
    _name = 'bs.sale.order.line'
    _rec_name = 'book_id'

    order_id = fields.Many2one('bs.sale.order')
    book_id = fields.Many2one('bs.book', required=True)
    qty = fields.Integer(default=1)
    unit_price = fields.Monetary()
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda s: s.env.company.currency_id)
    total_amount = fields.Monetary(compute='_compute_total_amount', store=True)

    @api.depends('qty', 'unit_price')
    def _compute_total_amount(self):
        for line in self:
            line.total_amount = line.qty * line.unit_price

    @api.onchange('book_id')
    def _onchange_book(self):
        self.unit_price = self.book_id.sale_price if self.book_id else 0
