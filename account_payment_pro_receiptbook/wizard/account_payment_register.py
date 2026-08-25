from odoo import models
from odoo.exceptions import ValidationError


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _get_receiptbook(self, partner_type):
        self.ensure_one()
        receiptbook = self.env["account.payment.receiptbook"].search(
            [
                ("partner_type", "=", partner_type),
                ("company_id", "=", self.company_id.id),
                ("company_id.use_receiptbook", "=", True),
            ],
            limit=1,
        )
        return receiptbook

    def _init_payments(self, to_process, edit_mode=False):
        if self.company_id.country_code == "AR":
            for rec in to_process:
                if rec.get("batch"):
                    if receiptbook := self._get_receiptbook(rec["batch"]["payment_values"]["partner_type"]):
                        if not receiptbook.sequence_id:
                            raise ValidationError(
                                self.env._(
                                    "Please define a sequence on receiptbook %(name)s.",
                                    name=receiptbook.display_name,
                                )
                            )
                        name = receiptbook.with_context(ir_sequence_date=self.payment_date).sequence_id.next_by_id()
                        rec["create_vals"]["name"] = "%s %s" % (receiptbook.document_type_id.doc_code_prefix, name)
                rec["create_vals"].setdefault("name", "/")
        return super()._init_payments(to_process, edit_mode=edit_mode)
