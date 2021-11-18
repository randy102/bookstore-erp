# -*- coding: utf-8 -*-

from odoo import models, fields


class Book(models.Model):
    _name = 'bs.book'
    _description = 'Book'
    _inherit = ['bs.sequence.name']
    _seq_code = 'bs.book'

    name = fields.Char()
    cover = fields.Image()
    date_published = fields.Date()
    page = fields.Integer()
    summary = fields.Html()
    size_x = fields.Float()
    size_y = fields.Float()
    size_z = fields.Float()
    stock_qty = fields.Integer(default=0, readonly=True)
    sale_price = fields.Monetary()
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda s: s.env.company.currency_id)

    author_ids = fields.Many2many('bs.author')
    active = fields.Boolean('Active', default=True)
