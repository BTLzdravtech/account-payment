import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add counterpart_exchange_rate to account_payment")
    openupgrade.add_columns(env, [
        ("account_payment", "counterpart_exchange_rate", "float"),
    ])
    _logger.info("END add counterpart_exchange_rate to account_payment")