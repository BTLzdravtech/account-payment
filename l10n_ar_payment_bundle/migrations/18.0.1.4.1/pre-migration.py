import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr


    _logger.info("START add is_main_payment to account_payment")
    openupgrade.add_columns(env, [
        ("account.payment", "is_main_payment", "boolean"),
    ])
    _logger.info("END add is_main_payment to account_payment")