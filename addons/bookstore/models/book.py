# -*- coding: utf-8 -*-

from odoo import models, fields


class Book(models.Model):
    _name = 'bs.book'
    _description = 'Book'

    name = fields.Char()
    cover = fields.Image()
    date_published = fields.Date()
    page = fields.Integer()
    summary = fields.Html()
    size_x = fields.Float()
    size_y = fields.Float()
    size_z = fields.Float()
    stock_qty = fields.Integer(default=0, readonly=True)

    author_ids = fields.Many2many('bs.author')
