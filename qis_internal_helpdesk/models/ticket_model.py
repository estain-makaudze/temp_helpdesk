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
    ], string='Priority', default='low', required=True)
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='Status', default='open', required=True)
    category = fields.Many2one('qis_internal_helpdesk.category_model', string='Category')
    company_id = fields.Many2one('res.company',string='Client',required=True,default=lambda self: self.env.company)
    sla_id = fields.Many2one('qis_internal_helpdesk.sla_model', string='SLA',)
    requester_name = fields.Many2one('qis_internal_helpdesk.clients_contacts', string='Requester Name')
    requester_email = fields.Char(related='requester_name.email', string='Requester Email', readonly=False)
    requester_phone = fields.Char(related='requester_name.phone', string='Requester Phone', readonly=False)

    # Assignment & Support Team
    assigned_id = fields.Many2one('res.users', string='Assigned')
    department = fields.Many2one('qis_internal_helpdesk.department_model', string='Department')

    # Timestamps & Tracking
    resolution_time = fields.Float(string='Resolution Time (Hours)', help='Time taken to resolve the ticket for SLA compliance')
    stage_change_date = fields.Datetime(string='Stage Change Date', default=fields.Datetime.now, readonly=True, help='When the ticket was last moved to the current stage')
    stage_age = fields.Integer(string='Stage Age (Hours)', compute='_compute_stage_age', store=True, help='Time in hours since the ticket entered the current stage')
    stage_age_display = fields.Char(string='Stage Age', compute='_compute_stage_age', store=True, help='Time in hours since the ticket entered the current stage')

    @api.depends('stage_change_date', 'status')
    def _compute_stage_age(self):
        now = fields.Datetime.now()
        for ticket in self:
            if ticket.stage_change_date and ticket.status != 'closed':
                delta = now - ticket.stage_change_date
                total_seconds = int(delta.total_seconds())
                ticket.stage_age = total_seconds // 3600  # Keep numeric hours for calculations
                
                # Calculate years, days, hours for human-readable format
                years = total_seconds // (365 * 24 * 3600)
                remaining_seconds = total_seconds % (365 * 24 * 3600)
                days = remaining_seconds // (24 * 3600)
                remaining_seconds %= (24 * 3600)
                hours = remaining_seconds // 3600
                
                # Build the display string
                parts = []
                if years > 0:
                    parts.append(f"{years} year{'s' if years > 1 else ''}")
                if days > 0:
                    parts.append(f"{days} day{'s' if days > 1 else ''}")
                if hours > 0 or not parts:  # Always show at least hours if no other parts
                    parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
                    
                ticket.stage_age_display = ', '.join(parts) if parts else '0 hours'
            else:
                ticket.stage_age = 0
                ticket.stage_age_display = '0 hours'

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        for rec in self:
            """ Automatically called when a new email is received """
            vals = {
                'title': msg_dict.get('subject') or 'No Subject',
                'description': msg_dict.get('body') or '',
                'requester_email': msg_dict.get('email_from'),
            }
            print("i have been run here")
            vals.update(custom_values or {})
            ticket = rec.create(vals)
            #send assigneme
        return ticket

    # @api.model_create_multi
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('helpdesk_ticket.seq')
        for rec in self:
            if rec.assigned_id:
                rec.email_template_ticket_assigned()
        return super(TicketModel, self).create(vals)

    def write(self, vals):
        # Update stage_change_date when status changes
        if 'status' in vals:
            vals['stage_change_date'] = fields.Datetime.now()
        res = super(TicketModel, self).write(vals)
        for rec in self:
            if rec.assigned_id:
                rec.email_template_ticket_assigned()
        return res

    def action_in_progress(self):
        """Move status to 'In Progress'"""
        self.write({'status': 'in_progress'})
        self.email_template_helpdesk_ticket_state_changed()


    def action_resolve(self):
        """Move status to 'Resolved'"""
        self.write({'status': 'resolved'})
        self.email_template_helpdesk_ticket_state_changed()


    def action_close(self):
        """Move status to 'Closed'"""
        self.write({'status': 'closed'})
        self.email_template_helpdesk_ticket_state_changed()


    def action_reopen(self):
        """Reopen a closed or resolved ticket"""
        self.write({'status': 'open'})
        self.email_template_helpdesk_ticket_state_changed()

    def action_ticket_acknowledgment_email(self):
        template = self.env.ref('qis_internal_helpdesk.email_template_helpdesk_ticket_acknowledgment')
        template.send_mail(self.id, force_send=True)


    def email_template_helpdesk_ticket_state_changed(self):
        template = self.env.ref('qis_internal_helpdesk.email_template_helpdesk_ticket_state_changed')
        template.send_mail(self.id, force_send=True)

    def email_template_ticket_assigned(self):
        template = self.env.ref('qis_internal_helpdesk.ticket_assigned_email_template')
        template.send_mail(self.id, force_send=True)