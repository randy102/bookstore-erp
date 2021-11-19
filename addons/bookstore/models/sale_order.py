from odoo import models, fields, api
from odoo.exceptions import UserError

SALE_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('delivered', 'Delivered')
]


class SaleOrder(models.Model):
    _name = 'bs.sale.order'
    _inherit = ['bs.sequence.code']
    _seq_code = 'bs.sale.order'
    _rec_name = 'code'

    customer_name = fields.Char(required=True)
    customer_address = fields.Text()
    customer_phone = fields.Char()
    state = fields.Selection(selection=SALE_STATES, default='draft')
    total_amount = fields.Monetary(compute='_compute_total_amount')
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda s: s.env.company.currency_id)
    date_confirmed = fields.Datetime(readonly=True)
    date_delivered = fields.Datetime(readonly=True)
    note = fields.Text()

    seller_id = fields.Many2one('bs.employee')
    line_ids = fields.One2many('bs.sale.order.line', 'order_id')
    transfer_ids = fields.One2many('bs.stock.transfer', 'sale_id')

    @api.model
    def create(self, vals):
        if not vals.get('seller_id'):
            employee = self.env['bs.employee'].search([('user_id', '=', self._uid)])
            vals['seller_id'] = employee.id if employee else False
        return super(SaleOrder, self).create(vals)

    def unlink(self):
        for sale in self:
            if 'confirmed' in sale.transfer_ids.mapped('state'):
                raise UserError('Can not delete order when transfer are confirmed')
        super(SaleOrder, self).unlink()

    @api.depends('line_ids.total_amount')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order.line_ids.mapped('total_amount'))

    def action_confirm(self):
        for order in self:
            order.state = 'confirmed'
            order.date_confirmed = fields.Datetime.now()
            self.env['bs.stock.transfer'].create_export(order)

    def action_open_transfer(self):
        return {
            'res_model': 'bs.stock.transfer',
            'type': 'ir.actions.act_window',
            'context': {'default_type': 'export'},
            'res_id': self.transfer_ids.id,
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("bookstore.bs_stock_transfer_form").id,
        }

    def action_print_invoice(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/html/bookstore.report_sale_order/{",".join(map(str, self.mapped("id")))}',
            'target': 'new'
        }
