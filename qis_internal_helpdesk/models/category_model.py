from odoo import fields, models, api


class CategoryModel(models.Model):
    _name = 'qis_internal_helpdesk.category_model'
    _description = 'Categories'

    name = fields.Char()
