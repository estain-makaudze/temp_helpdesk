# -*- coding: utf-8 -*-
# from odoo import http


# class QisInternalHelpdesk(http.Controller):
#     @http.route('/qis_internal_helpdesk/qis_internal_helpdesk', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qis_internal_helpdesk/qis_internal_helpdesk/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('qis_internal_helpdesk.listing', {
#             'root': '/qis_internal_helpdesk/qis_internal_helpdesk',
#             'objects': http.request.env['qis_internal_helpdesk.qis_internal_helpdesk'].search([]),
#         })

#     @http.route('/qis_internal_helpdesk/qis_internal_helpdesk/objects/<model("qis_internal_helpdesk.qis_internal_helpdesk"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qis_internal_helpdesk.object', {
#             'object': obj
#         })

