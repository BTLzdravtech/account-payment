import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr


    _logger.info("START add cashbox_session_id to account_payment")
    openupgrade.add_columns(env, [
        ("account_payment", "cashbox_session_id", "many2one"),
    ])
    _logger.info("END add cashbox_session_id to account_payment")