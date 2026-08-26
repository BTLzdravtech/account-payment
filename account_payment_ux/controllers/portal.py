from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request


class PortalAccountInherit(PortalAccount):
    # Obtiene el dominio de facturas vencidas y excluye las que tienen
    # pagos online pendientes (no manual/transferencia); esta busqueda
    # es necesaria porque el usuario portal no accede a payment.transaction.
    def _get_overdue_invoices_domain(self, partner_id=None):
        domain = super()._get_overdue_invoices_domain(partner_id=partner_id)
        company = request.env.company
        if company.country_code != "AR":
            return domain

        moves = request.env["account.move"].search(domain)
        if not moves:
            return domain

        pending_transactions = (
            request.env["payment.transaction"]
            .sudo()
            .search(
                [
                    ("company_id", "=", company.id),
                    ("invoice_ids", "in", moves.ids),
                    ("provider_code", "not in", ["manual", "transfer"]),
                    ("state", "=", "pending"),
                ]
            )
        )
        ignored_moves = (pending_transactions.invoice_ids & moves).ids
        if ignored_moves:
            domain = domain + [("id", "not in", ignored_moves)]
        return domain
