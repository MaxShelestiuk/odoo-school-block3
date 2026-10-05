from odoo import api, fields, models


class HospitalDoctorHistory(models.Model):
    _name = 'hospital.doctor.history'
    _description = 'Personal Doctor History'
    _rec_names_search = ['patient_id.name', 'doctor_id.name']

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Пацієнт',
        required=True,
        ondelete='restrict',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар',
        required=True,
        ondelete='restrict',
    )
    assignment_date = fields.Date(
        string='Дата призначення',
        required=True,
        default=fields.Date.today,
    )
    change_date = fields.Date(string='Дата зміни лікаря')
    active = fields.Boolean(string='Активний', default=True)

    @api.onchange('assignment_date', 'change_date')
    def _onchange_dates(self):
        if (
            self.assignment_date
            and self.change_date
            and self.change_date < self.assignment_date
        ):
            return {
                'warning': {
                    'title': 'Некоректні дати',
                    'message': (
                        'Дата зміни лікаря не може бути раніше '
                        'ніж дата призначення'
                    ),
                },
            }

    @api.depends(
        'patient_id.name',
        'doctor_id.name',
        'doctor_id.category_id.name',
        'assignment_date',
    )
    def _compute_display_name(self):
        for record in self:
            patient_name = record.patient_id.name or ''
            doctor_name = record.doctor_id.name or ''
            category_name = record.doctor_id.category_id.name or ''
            assignment_date = (
                fields.Date.to_string(record.assignment_date)
                if record.assignment_date
                else ''
            )
            record.display_name = (
                f'{patient_name} - {doctor_name} '
                f'({category_name}) {assignment_date}'
            )
