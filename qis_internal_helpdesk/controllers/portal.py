from odoo import http
from odoo.http import request

class HelpdeskPortalController(http.Controller):

    @http.route(['/my/helpdesk/submit'], type='http', auth='public', website=True)
    def portal_submit_ticket_form(self, **kwargs):
        """ Show the form to submit a ticket """
        return request.render('qis_internal_helpdesk.portal_ticket_submit', {})

    @http.route(['/my/helpdesk/submit/submit'], type='http', auth='public', website=True, csrf=True)
    def portal_submit_ticket(self, **post):
        """ Handle form submission """
        # handle client creation into clients model
        clients_contact_id = request.env["qis_internal_helpdesk.clients_contacts"].search(
            [('email', '=', post.get('requester_email'))], limit=1
        )
        if not clients_contact_id:
            request.env['qis_internal_helpdesk.clients_contacts'].create({
                'name': clients_contact_id.name,
                'email': post.get('requester_email'),
                'phone': post.get('requester_phone'),
                'company_id': request.env.company.id,
            })
        ticket = request.env['qis_internal_helpdesk.ticket_model'].sudo().create({
            'title': post.get('title'),
            'description': post.get('description'),
            'requester_name': clients_contact_id.id,
            'company_id': request.env.company.id,
        })
        ticket.action_ticket_acknowledgment_email()

        #send an acknowledgment email
        return request.render('qis_internal_helpdesk.portal_ticket_thank_you', {'ticket': ticket})
