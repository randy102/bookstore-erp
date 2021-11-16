from odoo import models, fields, api

SALE_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('delivered', 'Delivered')
]


class SaleOrder(models.Model):
    _name = 'bs.sale.order'

    name = fields.Char(readonly=True)
    customer_name = fields.Char()
    customer_address = fields.Text()
    customer_phone = fields.Char()
    state = fields.Selection(selection=SALE_STATES, default='draft')
    total_amount = fields.Monetary(compute='_compute_total_amount')
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda s: s.env.company.currency_id)
    date_confirmed = fields.Datetime(readonly=True)
    date_delivered = fields.Datetime(readonly=True)

    seller_id = fields.Many2one('bs.employee')
    line_ids = fields.One2many('bs.sale.order.line', 'order_id')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('bs.sale.order')
        return super(SaleOrder, self).create(vals)

    def action_confirmed(self):
        for order in self:
            order.state = 'confirmed'
            order.date_confirmed = fields.Datetime.now()
            # TODO: Create Stock Transfer

    @api.depends('line_ids.total_amount')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order.line_ids.mapped('total_amount'))
