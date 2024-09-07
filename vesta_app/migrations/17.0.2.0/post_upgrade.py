import logging
# from odoo.upgrade import util
from odoo import api

_logger = logging.getLogger(__name__)


def post_upgrade(cr, registry):
    """Perform data migration after module upgrade."""
    env = api.Environment(cr, api.SUPERUSER_ID, registry)

    # Retrieve studio fields
    # get_studio_fields(env, 'product.template')

    # Define field mappings and perform the migration
    field_mappings = {
        'x_studio_product_code': 'va_product_code',
        'x_studio_is_featured': 'va_is_featured',
        'x_studio_weight': 'va_weight',
    }

    for old_field, new_field in field_mappings.items():
        products = env['product.template'].search([(old_field, '!=', False)])
        for product in products:
            old_value = getattr(product, old_field, False)
            if old_value:
                setattr(product, new_field, old_value)
                product.save()  # Ensure changes are saved
        _logger.info(f"Migrated {old_field} to {new_field}. Updated {len(products)} records.")