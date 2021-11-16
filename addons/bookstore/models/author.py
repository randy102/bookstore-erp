from odoo import models, fields


class Author(models.Model):
    _name = 'bs.author'

    name = fields.Char()
    date_of_birth = fields.Date()
    book_ids = fields.Many2many('bs.book')
