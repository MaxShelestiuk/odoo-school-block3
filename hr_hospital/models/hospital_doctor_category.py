from odoo import fields, models


class HospitalDoctorCategory(models.Model):
    _name = 'hospital.doctor.category'
    _description = 'Doctor Qualification'
    _order = 'sequence, name, id'

    name = fields.Char(string='Назва', required=True)
    sequence = fields.Integer(string='Послідовність', default=10)
    is_intern = fields.Boolean(string='Категорія інтерна')
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='category_id',
        string='Лікарі',
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Назва кваліфікації вже існує!',
    )
