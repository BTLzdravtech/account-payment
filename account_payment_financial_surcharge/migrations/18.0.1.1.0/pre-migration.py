import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add card_id and installment_id to account_payment")
    openupgrade.add_columns(env, [
        ("account_payment", "card_id", "many2one"),
    ])
    _logger.info("END add card_id and installment_id to account_payment")

    _logger.info("START add installment_id to account_payment")
    openupgrade.add_columns(env, [
        ("account_payment", "installment_id", "many2one"),
    ])
    _logger.info("END add installment_id to account_payment")