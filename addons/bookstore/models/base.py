from odoo import models, fields, api


class SequenceName(models.AbstractModel):
    _name = 'bs.sequence.name'
    _seq_code = ''

    name = fields.Char(readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(self._seq_code)
        return super(SequenceName, self).create(vals)
