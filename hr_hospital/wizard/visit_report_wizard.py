from datetime import datetime, time, timedelta

import pytz

from odoo import api, fields, models
from odoo.exceptions import UserError


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Patient Visit Report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Лікарі',
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Пацієнти',
    )
    date_from = fields.Date(
        string='Початок періоду',
        help='За запланованою датою візиту, у вашому часовому поясі.',
    )
    date_to = fields.Date(
        string='Кінець періоду',
        help='Останній день включається повністю.',
    )
    only_done = fields.Boolean(
        string='Лише завершені візити',
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Хвороба',
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []

        if not active_ids:
            active_id = self.env.context.get('active_id')
            active_ids = [active_id] if active_id else []

        if (
            active_model == 'hr.hospital.doctor'
            and 'doctor_ids' in fields_list
        ):
            doctors = self.env['hr.hospital.doctor'].browse(
                active_ids
            ).exists()
            values['doctor_ids'] = [fields.Command.set(doctors.ids)]

        elif (
            active_model == 'hr.hospital.patient'
            and 'patient_ids' in fields_list
        ):
            patients = self.env['hr.hospital.patient'].browse(
                active_ids
            ).exists()
            values['patient_ids'] = [fields.Command.set(patients.ids)]

        return values

    def action_show_visits(self):
        self.ensure_one()

        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise UserError(
                self.env._(
                    'Початок періоду не може бути пізніше кінця періоду.'
                )
            )

        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))

        if self.only_done:
            domain.append(('state', '=', 'done'))

        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))

        timezone_name = (
            self.env.context.get('tz')
            or self.env.user.tz
            or 'UTC'
        )
        user_timezone = pytz.timezone(timezone_name)

        if self.date_from:
            local_start = user_timezone.localize(
                datetime.combine(self.date_from, time.min)
            )
            utc_start = local_start.astimezone(pytz.UTC).replace(
                tzinfo=None
            )
            domain.append((
                'visit_datetime',
                '>=',
                fields.Datetime.to_string(utc_start),
            ))

        if self.date_to:
            next_day = self.date_to + timedelta(days=1)
            local_end = user_timezone.localize(
                datetime.combine(next_day, time.min)
            )
            utc_end = local_end.astimezone(pytz.UTC).replace(
                tzinfo=None
            )
            domain.append((
                'visit_datetime',
                '<',
                fields.Datetime.to_string(utc_end),
            ))

        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Візити за вибраними критеріями'),
            'res_model': 'hr.hospital.patient.visit',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': domain,
            'context': {'active_test': True},
        }
