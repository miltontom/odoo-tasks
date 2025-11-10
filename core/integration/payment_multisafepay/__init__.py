from . import models
from . import controllers

from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    setup_provider(env, 'multisafepay')
    record = env['payment.provider'].search([('code', '=', 'multisafepay')])
    record.write({
        'redirect_form_view_id': env.ref('payment_multisafepay.redirect_form')
    })


def uninstall_hook(env):
    reset_payment_provider(env, 'multisafepay')