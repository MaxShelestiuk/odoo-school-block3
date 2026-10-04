from odoo import fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hospital.medic.info'
    _description = 'Hospital Patient'

    name = fields.Char(required=True)