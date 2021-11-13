# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Book(models.Model):
    _name = 'bs.book'
    _description = 'Book'

    name = fields.Char()
    cover = fields.Image()
    date_published = fields.Date()
