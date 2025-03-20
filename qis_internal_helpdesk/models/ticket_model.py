from odoo import models, fields, api


class TicketModel(models.Model):
    _name = 'qis_internal_helpdesk.ticket_model'
    _description = 'Helpdesk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Ticket No.', required=True, copy=False, readonly=True, default='New')
    title = fields.Char(string='Title', required=True)
    description = fields.Html(string='Description')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], string='Priority', default='medium', required=True)
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='Status', default='open', required=True)
    category = fields.Many2one('qis_internal_helpdesk.category_model', string='Category', required=True)

    customer = fields.Many2one('res.partner', string='Customer', required=True)
    sla_id = fields.Many2one('qis_internal_helpdesk.sla_model', string='SLA', required=True)
    requester_name = fields.Char(string='Requester Name', required=True)
    requester_email = fields.Char(string='Requester Email', required=True)
    requester_phone = fields.Char(string='Requester Phone')

    # Assignment & Support Team
    assigned_id = fields.Many2one('res.users', string='Assigned')
    department = fields.Many2one('qis_internal_helpdesk.department_model', string='Department')

    # Timestamps & Tracking
    resolution_time = fields.Float(string='Resolution Time (Hours)',help='Time taken to resolve the ticket for SLA compliance')

    # @api.model_create_multi
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('helpdesk_ticket.seq')
        return super(TicketModel, self).create(vals)

    def action_in_progress(self):
        """Move status to 'In Progress'"""
        self.write({'status': 'in_progress'})

    def action_resolve(self):
        """Move status to 'Resolved'"""
        self.write({'status': 'resolved'})

    def action_close(self):
        """Move status to 'Closed'"""
        self.write({'status': 'closed'})

    def action_reopen(self):
        """Reopen a closed or resolved ticket"""
        self.write({'status': 'open'})