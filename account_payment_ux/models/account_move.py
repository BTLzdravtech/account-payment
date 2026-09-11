from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _has_to_be_paid(self):
        self.ensure_one()
        if self.company_id.country_code != "AR":
            return super()._has_to_be_paid()

        pending_transactions = self.transaction_ids.filtered(
            lambda tx: tx.state == "pending" and tx.provider_code not in ["manual", "transfer"]
        )
        return not pending_transactions and super()._has_to_be_paid()
