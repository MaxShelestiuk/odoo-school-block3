from odoo import api, fields, models
from odoo.exceptions import UserError


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

    def write(self, vals):
        completed_visits = self.filtered(lambda visit: visit.state == 'done')

        if completed_visits:
            if 'state' in vals and vals['state'] != 'done':
                raise UserError('Не можна змінювати статус завершеного візиту.')

            if 'active' in vals and not vals['active']:
                raise UserError('Не можна архівувати завершений візит.')

            for visit in completed_visits:
                if ('doctor_id' in vals and vals['doctor_id'] != visit.doctor_id.id):
                    raise UserError('Не можна змінювати лікаря завершеного візиту.')

                for field_name in ('visit_datetime', 'actual_visit_datetime',):
                    if field_name not in vals:
                        continue

                    new_value = (fields.Datetime.to_datetime(vals[field_name]) or False)
                    if new_value != visit[field_name]:
                        raise UserError(
                            'Не можна змінювати дату або час '
                            'завершеного візиту.'
                        )

        return super().write(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_completed(self):
        if any(visit.state == 'done' for visit in self):
            raise UserError(
                'Не можна видаляти завершений візит.'
            )