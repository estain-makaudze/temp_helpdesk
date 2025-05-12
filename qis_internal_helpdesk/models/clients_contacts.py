from odoo import fields, models, api


class ClientsContacts(models.Model):
    _name = 'qis_internal_helpdesk.clients_contacts'
    _description = 'Client Contact'

    name = fields.Char(string="Name")
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone")
    company_id = fields.Many2one('res.company',string='Client',required=True,default=lambda self: self.env.company)


