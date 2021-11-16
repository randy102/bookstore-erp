from odoo import models, fields

DEPARTMENTS = [
    ('sale', 'Sale'),
    ('purchase', 'Purchase'),
    ('inventory', 'Inventory'),
]


class Employee(models.Model):
    _name = 'bs.employee'

    name = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    address = fields.Text()
    department = fields.Selection(selection=DEPARTMENTS)
    user_id = fields.Many2one('res.users', readonly=True)

    def action_create_user(self):
        for employee in self:
            user = self.env['res.users'].create({'login': employee.email, 'name': employee.name})
            employee.user_id = user.id
