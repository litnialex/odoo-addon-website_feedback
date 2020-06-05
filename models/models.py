# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Feedback(models.Model):
    _name = 'website_feedback.feedback'
    website_form_recaptcha = True

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    state = fields.Selection([
        ('approved', 'Approved'),
        ('unapproved', 'Unapproved')],
        string='Status', default='unapproved', readonly=False)
    email = fields.Char(default='')
    company_name = fields.Char()
    feedback = fields.Text(required=True)
    date = fields.Date(default=fields.Datetime.now())
    prooflink = fields.Char()
