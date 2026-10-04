from odoo import fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hospital.medic.info'
    _description = 'Hospital Patient'

    name = fields.Char(required=True)
    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Персональний лікар',
        ondelete='restrict',
    )
    doctor_history_ids = fields.One2many(
        comodel_name='hospital.doctor.history',
        inverse_name='patient_id',
        string='Історія персональних лікарів',
    )
    insurance_policy_number = fields.Char(
        string='Номер страхового поліса',
        size=20,
    )