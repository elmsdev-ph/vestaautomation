from odoo import models, fields, api
# from odoo.upgrade.util import fields as upgrade_fields
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    va_product_code = fields.Char(string="Product Code")
    va_is_featured = fields.Boolean(string="is Featured?", default=False)
    va_weight = fields.Integer(string="Weight")

    def _migrate_product_template_fields(self):
        """Perform data migration after module upgrade."""
        # Define field mappings and perform the migration
        field_mappings = {
            'x_studio_product_code': 'va_product_code',
            'x_studio_is_featured': 'va_is_featured',
            'x_studio_weight': 'va_weight',
        }

        for old_field, new_field in field_mappings.items():
            products = self.env['product.template'].search([(old_field, '!=', False)])
            for product in products:
                old_value = getattr(product, old_field, False)
                if old_value:
                    setattr(product, new_field, old_value)
                    # product.save()  # Ensure changes are saved
            _logger.info(f"Migrated {old_field} to {new_field}. Updated {len(products)} records.")

    def _get_studio_fields(self):
        """Identify and return studio fields from the model."""
        studio_fields = [field for field in self._fields if field.startswith('x_studio_')]
        _logger.info(f"List of fields: {studio_fields}")
        return studio_fields

    def _drop_x_studio_columns(self):
        """Drop all columns starting with 'x_studio_' from product_template."""
        table_name = 'product_template'
        self.env.cr.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s AND column_name LIKE 'x_studio_%%'
        """, (table_name,))
        columns_to_drop = self.env.cr.fetchall()

        if columns_to_drop:
            for column in columns_to_drop:
                col_name = column[0]
                drop_query = f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {col_name};"
                self.env.cr.execute(drop_query)
                _logger.info(f"Dropped column {col_name} from {table_name}")
        else:
            _logger.info("No columns found with prefix 'x_studio_' to drop.")
