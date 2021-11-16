from odoo import models, fields


class Supplier(models.Model):
    _name = 'bs.supplier'

    name = fields.Char()
    phone = fields.Char()
    address = fields.Text()
