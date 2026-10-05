from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'

    name = fields.Char(required=True)
    complete_name = fields.Char(
        string='Повна назва',
        compute='_compute_complete_name',
        store=True,
        recursive=True,
    )
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

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for disease in self:
            name = disease.name or ''
            if disease.parent_id:
                disease.complete_name = (
                    f'{disease.parent_id.complete_name} / {name}'
                )
            else:
                disease.complete_name = name

    @api.depends('complete_name')
    def _compute_display_name(self):
        for disease in self:
            disease.display_name = disease.complete_name or ''

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if self._has_cycle():
            raise ValidationError(
                'Не можна створювати циклічну ієрархію хвороб.'
            )
