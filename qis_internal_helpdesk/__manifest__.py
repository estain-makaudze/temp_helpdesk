# -*- coding: utf-8 -*-
{
    'name': "QIS Internal Helpdesk",
    'summary': "QIS helpdesk for managing customers tickets",
    'description': """
        A helpdesk module for managing QIS Solutions Customers and tracking their SLA's
    """,
    'author': "Estain Makaudze",
    'website': "https://www.qis.com",
    'category': 'Helpdesk',
    'version': '18.1',
    'depends': ['base','mail','contacts','website'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/ticket_model.xml',
        'views/department_model.xml',
        'views/category_model.xml',
        'views/sla_model.xml',
        'views/portal.xml',
        'views/clients_contacts.xml',
        'views/ticket_acknowledgment_email_template.xml',
        'views/ticket_state_changed_email_template.xml',
        'views/ticket_assigned_email_template.xml',
    ],
    'license': 'OPL-1',
}