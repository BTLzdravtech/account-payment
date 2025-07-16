from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # @api.model
    # def get_view(self, view_id=None, view_type="form", **options):
    #     if view_type == "form" and self.env.company.country_code == "AR":
    #         view_id = self.env.ref("account_payment_financial_surcharge.view_move_form_ar").id
    #     return super().get_view(view_id=view_id, view_type=view_type, **options)
