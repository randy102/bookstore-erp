from odoo import models, fields, api
from odoo.exceptions import UserError

PURCHASE_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('received', 'Received')
]


class PurchaseOrder(models.Model):
    _name = 'bs.purchase.order'
    _inherit = ['bs.sequence.code']
    _seq_code = 'bs.purchase.order'
    _rec_name = 'code'

    state = fields.Selection(selection=PURCHASE_STATES, default='draft')
    total_amount = fields.Monetary(compute='_compute_total_amount')
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda s: s.env.company.currency_id)
    date_confirmed = fields.Datetime(readonly=True)
    date_received = fields.Datetime(readonly=True)
    note = fields.Text()

    buyer_id = fields.Many2one('bs.employee')
    supplier_id = fields.Many2one('bs.supplier', required=True)
    line_ids = fields.One2many('bs.purchase.order.line', 'order_id')
    transfer_ids = fields.One2many('bs.stock.transfer', 'purchase_id')

    @api.model
    def create(self, vals):
        if not vals.get('buyer_id'):
            employee = self.env['bs.employee'].search([('user_id', '=', self._uid)])
            vals['buyer_id'] = employee.id if employee else False
        return super(PurchaseOrder, self).create(vals)

    def unlink(self):
        for purchase in self:
            if 'confirmed' in purchase.transfer_ids.mapped('state'):
                raise UserError('Can not delete order when transfer are confirmed')
        super(PurchaseOrder, self).unlink()

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

    @api.depends('line_ids.total_amount')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order.line_ids.mapped('total_amount'))

    def action_print_invoice(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/html/bookstore.report_purchase_order/{",".join(map(str, self.mapped("id")))}',
            'target': 'new'
        }
