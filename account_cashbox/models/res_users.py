##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_cashbox_ids = fields.Many2many(
        'account.cashbox',
        relation='account_cashbox_users_rel',
        column1='user_id',
        column2='cashbox_id',
    )
    requiere_account_cashbox_session = fields.Boolean()

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        if view_type == "form" and self.env.company.country_code == "AR":
            view_id = self.env.ref("account_cashbox.view_users_form_extend_ar").id
        return super().get_view(view_id=view_id, view_type=view_type, **options)