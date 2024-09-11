# -*- coding: utf-8 -*-
from . import models
from odoo import api, SUPERUSER_ID
from . import migrations
import logging


_logger = logging.getLogger(__name__)

"""
    STEPS OF DATA MIGRATIONS PROCESS
    1. Mapping of the existing studio fields
    2. Migrate the data of x_studio field to the new field of va_
    3. Dropping table columns that starts with x_studio_ fields
        Note: Make sure to uninstall the studio customization module to avoid error in the views
"""


def _get_studio_fields(env):
    """Identify and return studio fields from multiple models."""
    models_to_check = ['product.template', 'product.product', 'sale.order', 'documents.document', 'project.project', 'project.task']
    studio_fields = {}

    for model_name in models_to_check:
        model_obj = env[model_name].search([])
        model_studio_fields = [field for field in model_obj._fields if field.startswith('x_studio_')]
        studio_fields[model_name] = model_studio_fields
        _logger.info(f"List of fields for {model_name}: {model_studio_fields}")

    return studio_fields


def get_studio_fields(env):
    """Identify and return studio fields from the model."""
    _get_studio_fields(env)


def _migrate_product_template(env):
    env['product.template']._migrate_product_template_fields()
    _logger.info("Data successfull migrated...")


def _migrate_studio_fields_data(env):
    env['product.product']._migrate_studio_fields()
    env['product.template']._migrate_studio_fields()
    env['documents.document']._migrate_studio_fields()
    env['project.project']._migrate_studio_fields()
    env['project.task']._migrate_studio_fields()
    _logger.info("Data successfull migrated...")


def _drop_studio_col_fields(env):
    env['product.template']._drop_x_studio_columns()
    env['product.product']._drop_x_studio_columns()
    env['documents.document']._drop_x_studio_columns()
    env['project.project']._drop_x_studio_columns()
    env['project.task']._drop_x_studio_columns()
    _logger.info("Successfully Droping table columns...")


def post_upgrade_hook(env):
    """Post-upgrade hook to run after upgrading the module."""
    _migrate_studio_fields_data(env)
    # Dropping tables columns that starts with x_studio fields
    # _drop_studio_col_fields(env)
