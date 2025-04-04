from odoo import models, fields


class ServiceLevelAgreementModel(models.Model):
    _name = 'qis_internal_helpdesk.sla_model'
    _description = 'Service Level Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='SLA Name', required=True)
    company_id = fields.Many2one('res.company',string='Client',required=True,default=lambda self: self.env.company)
    response_time = fields.Float(string='Response Time (Hours)', help='Maximum time allowed to respond to a ticket')
    resolution_time = fields.Float(string='Resolution Time (Hours)', help='Maximum time allowed to resolve a ticket')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], string='Priority', required=True)
    active = fields.Boolean(string='Active', default=True)
    ticket_ids = fields.One2many('qis_internal_helpdesk.ticket_model', 'sla_id', string='Tickets')
