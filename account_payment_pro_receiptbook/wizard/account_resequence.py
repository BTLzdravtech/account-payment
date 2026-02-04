import json

from odoo import _, models
from odoo.exceptions import ValidationError, UserError


class ReSequenceWizard(models.TransientModel):
    _inherit = "account.resequence.wizard"

    def resequence(self):
        # DONETODO: Odoo BTL - needs to be locked on AR company
        if self.env.company.country_code == 'AR':
            if self.ordering == "keep":
                new_names = [v["new_by_name"] for v in json.loads(self[0]["new_values"]).values()]
            else:
                new_names = [v["new_by_date"] for v in json.loads(self[0]["new_values"]).values()]

            duplicated_names = self.env["account.move"].search(
                [
                    ("receiptbook_id", "=", self.move_ids.receiptbook_id.id),
                    ("name", "in", new_names),
                    ("id", "not in", self.move_ids.ids),
                ]
            )
            if duplicated_names:
                raise ValidationError(
                    _("The following receipt names already exist:\n%s") % "\n".join(duplicated_names.mapped("name"))
                )

            original_move_ids = self.move_ids
            original_wizard = self[0].copy()

            for journal in original_move_ids.journal_id:
                move_ids = original_move_ids.filtered(lambda x: x.journal_id == journal)

                all_moves = json.loads(original_wizard.read()[0]["new_values"])

                # Filter only the moves for this journal
                filtered_moves = {str(mid.id): all_moves[str(mid.id)] for mid in move_ids if str(mid.id) in all_moves}

                # I have to write move_ids before new_values because is computed
                # and changes new_values
                self[0].write({"move_ids": move_ids})
                # Write as proper JSON string
                self[0].write({"new_values": json.dumps(filtered_moves)})

                super().resequence()
        else:
            super().resequence()


    def default_get(self, fields_list):
        values = super(ReSequenceWizard, self).default_get(fields_list)
        # DONETODO: Odoo BTL - needs to be locked on AR company
        if self.env.company.country_code == 'AR':

            if "move_ids" not in fields_list:
                return values
            active_move_ids = self.env["account.move"]
            if self.env.context["active_model"] == "account.move" and "active_ids" in self.env.context:
                active_move_ids = self.env["account.move"].browse(self.env.context["active_ids"])

            # Comprobamos si todos los diarios tienen el mismo receiptbook
            if all(move.receiptbook_id for move in active_move_ids):
                if len(active_move_ids.receiptbook_id) > 1:
                    raise UserError(_("You can only resequence items from the same receiptbook"))
            elif any(move.receiptbook_id for move in active_move_ids):
                raise UserError(
                    _(
                        "You can only resequence items if all selected moves belong to the same receiptbook, or if none have a receiptbook assigned."
                    )
                )
            else:
                # Métodoo original de odoo
                if len(active_move_ids.journal_id) > 1:
                    raise UserError(_("You can only resequence items from the same journal"))
                move_types = set(active_move_ids.mapped("move_type"))
                if (
                    active_move_ids.journal_id.refund_sequence
                    and ("in_refund" in move_types or "out_refund" in move_types)
                    and len(move_types) > 1
                ):
                    raise UserError(
                        _(
                            "The sequences of this journal are different for Invoices and Refunds but you selected some of both types."
                        )
                    )
                is_payment = set(active_move_ids.mapped(lambda x: bool(x.origin_payment_id)))
                if active_move_ids.journal_id.payment_sequence and len(is_payment) > 1:
                    raise UserError(
                        _(
                            "The sequences of this journal are different for Payments and non-Payments but you selected some of both types."
                        )
                    )

            values["move_ids"] = [(6, 0, active_move_ids.ids)]

        return values