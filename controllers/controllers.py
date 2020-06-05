# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

class WebsiteFeedback(http.Controller):
    @http.route('/feedback/', auth='public', website=True, methods=['POST', 'GET'], csrf=True)
    def index(self, **post):
        if http.request.httprequest.method == 'GET':
            return http.request.render('website_feedback.index', {
                'feedback_set': http.request.env['website_feedback.feedback'].search([]),
                })
        elif http.request.httprequest.method == 'POST':
            logger.info('=========== google recaptcha response is: {}'.format(post.get('g-recaptcha-response')))
            try:
              http.request.env['website.form.recaptcha'].action_validate(post.get('g-recaptcha-response'), http.request.httprequest.remote_addr)
            except ValidationError as e:
              logger.info('=========== google recaptcha validation error: {}'.format(e))
              return http.request.render('website.http_error', {'status_message': 'Google Captcha Validation Error: {}'.format(e)})
              
            feedback_submitted = http.request.env['website_feedback.feedback'].sudo().create({
                'name': post.get('name'), 'email': post.get('email'),
                'company_name': post.get('company_name'), 'feedback': post.get('feedback'),
                })

            #Feedback Notification Email
            template_id = http.request.env['mail.template'].sudo().search([('name', 'ilike', 'Feedback Notification')], limit=1)[0]
            logger.info('=========template_id is: {}'.format(template_id))
            if template_id:
                template_id.send_mail(feedback_submitted.id, True, True)

            return http.request.render('website_feedback.index', {
                'feedback_set': http.request.env['website_feedback.feedback'].search([]),
                'feedback_submitted': feedback_submitted,
                })

