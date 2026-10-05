from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'

    name = fields.Char(required=True)
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Батьківська хвороба',
        ondelete='restrict',
        index=True,
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Дочірні хвороби',
    )

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if self._has_cycle():
            raise ValidationError(
                'Не можна створювати циклічну ієрархію хвороб.'
            )