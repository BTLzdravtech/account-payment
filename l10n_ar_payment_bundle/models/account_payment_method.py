from odoo import api, models


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        # TODO: Odoo BTL - needs to be locked on AR company
        res["payment_bundle"] = {"mode": "unique", "type": ("cash",)}
        return res
