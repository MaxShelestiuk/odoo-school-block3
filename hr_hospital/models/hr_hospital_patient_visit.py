from odoo import fields, models


class HrHospitalPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient Visit'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('planned', 'Заплановано'),
            ('done', 'Завершено'),
            ('cancelled', 'Скасовано'),
        ],
        string='Статус',
        required=True,
        default='planned',
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Пацієнт',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар',
    )
    visit_datetime = fields.Datetime(
        string='Запланована дата та час',
    )
    actual_visit_datetime = fields.Datetime(
        string='Фактична дата та час',
    )
    summary = fields.Html(string='Епікриз')
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Хвороба',
        ondelete='restrict',
    )