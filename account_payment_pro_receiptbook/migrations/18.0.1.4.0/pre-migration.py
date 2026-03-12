import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add receiptbook_id to account_move")
    openupgrade.add_columns(env, [
        ("account.move", "receiptbook_id", "many2one"),
    ])

    _logger.info("END add receiptbook_id to account_move")


    _logger.info("START add receiptbook_id to account_payment")
    openupgrade.add_columns(env, [
        ("account.payment", "receiptbook_id", "many2one"),
    ])
    _logger.info("END add receiptbook_id to account_payment")


    _logger.info("START set receiptbook_id to account_move")
    openupgrade.logged_query(cr, """
        UPDATE account_move am
           SET receiptbook_id = ap.receiptbook_id
          FROM account_payment ap
         WHERE am.id = ap.move_id
           AND am.receiptbook_id IS NULL
           AND ap.receiptbook_id IS NOT NULL
    """)
    _logger.info("END set receiptbook_id to account_move")
