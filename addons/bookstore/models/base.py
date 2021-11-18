from odoo import models, fields, api


class SequenceName(models.AbstractModel):
    _name = 'bs.sequence.name'
    _seq_code = ''

    code = fields.Char(readonly=True)

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code(self._seq_code)
        return super(SequenceName, self).create(vals)
