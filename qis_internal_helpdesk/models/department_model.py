from odoo import fields, models, api


class DepartmentModel(models.Model):
    _name = 'qis_internal_helpdesk.department_model'
    _description = 'Department'

    name = fields.Char()
