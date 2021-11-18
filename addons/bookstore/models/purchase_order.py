from odoo import models, fields, api
from odoo.exceptions import UserError

PURCHASE_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('received', 'Received')
]


class PurchaseOrder(models.Model):
    _name = 'bs.purchase.order'
    _inherit = ['bs.sequence.name']
    _seq_code = 'bs.purchase.order'
    _rec_name = 'code'

    state = fields.Selection(selection=PURCHASE_STATES, default='draft')
    total_amount = fields.Monetary(compute='_compute_total_amount')
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda s: s.env.company.currency_id)
    date_confirmed = fields.Datetime(readonly=True)
    date_received = fields.Datetime(readonly=True)

    buyer_id = fields.Many2one('bs.employee')
    supplier_id = fields.Many2one('bs.supplier')
    line_ids = fields.One2many('bs.purchase.order.line', 'order_id')
    transfer_ids = fields.One2many('bs.stock.transfer', 'purchase_id')

    def action_confirm(self):
        for order in self:
            order.state = 'confirmed'
            order.date_confirmed = fields.Datetime.now()
            self.env['bs.stock.transfer'].create_import(order)

    def action_open_transfer(self):
        return {
            'res_model': 'bs.stock.transfer',
            'type': 'ir.actions.act_window',
            'context': {'default_type': 'import'},
            'res_id': self.transfer_ids.id,
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("bookstore.bs_stock_transfer_form").id,
        }

    def unlink(self):
        for purchase in self:
            if 'confirmed' in purchase.transfer_ids.mapped('state'):
                raise UserError('Can not delete order when transfer are confirmed')
        super(PurchaseOrder, self).unlink()

    @api.depends('line_ids.total_amount')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order.line_ids.mapped('total_amount'))
