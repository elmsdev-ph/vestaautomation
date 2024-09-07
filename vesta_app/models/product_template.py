from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # New Text
    va_char_field_om_1h93mu83u = fields.Char(string='New Text', store=True)

    # Cut Sheet
    va_cut_sheet = fields.Binary(string='Cut Sheet', store=True)

    # Filename for Cut Sheet
    va_cut_sheet_filename = fields.Char(string='Filename for Cut Sheet', store=True)

    # Additional Notes
    va_description = fields.Char(string='Additional Notes', store=True)

    # MFR Number
    va_mfr_number = fields.Char(string='MFR Number', store=True)

    # Preferred Vendor (Selection field)
    va_preferred_vendor = fields.Selection([
        ('vendor1', 'Vendor 1'),
        ('vendor2', 'Vendor 2'),
        ('vendor3', 'Vendor 3')
    ], string='Preferred Vendor', store=True)

    # Product Code
    va_product_code = fields.Char(string='Product Code', store=True)

    # New Related Field (Many2one to product.product)
    va_related_field_20v_1hcvakv6c = fields.Many2one('product.product', string='New Related Field', readonly=True)

    # Supplier's Code
    va_suppliers_code = fields.Char(string="Supplier's Code", store=True)

    # Supplier's Webpage
    va_suppliers_webpage = fields.Char(string="Supplier's Webpage", store=True)

    def _migrate_studio_fields(self):
        """Perform data migration after module upgrade."""
        # Define field mappings and perform the migration
        field_mappings = {
            'x_studio_char_field_om_1h93mu83u': 'va_char_field_om_1h93mu83u',
            'x_studio_cut_sheet': 'va_cut_sheet',
            'x_studio_cut_sheet_filename': 'va_cut_sheet_filename',
            'x_studio_description': 'va_description',
            'x_studio_mfr_number': 'va_mfr_number',
            'x_studio_preferred_vendor': 'va_preferred_vendor',
            'x_studio_product_code': 'va_product_code',
            'x_studio_related_field_20v_1hcvakv6c': 'va_related_field_20v_1hcvakv6c',
            'x_studio_suppliers_code': 'va_suppliers_code',
            'x_studio_suppliers_webpage': 'va_suppliers_webpage',
        }
        for old_field, new_field in field_mappings.items():
            products = self.env['product.template'].search([(old_field, '!=', False)])
            for product in products:
                old_value = getattr(product, old_field, False)
                if old_value:
                    setattr(product, new_field, old_value)
                    # product.save()  # Ensure changes are saved
            _logger.info(f"Migrated {old_field} to {new_field}. Updated {len(products)} records.")

    def _drop_x_studio_columns(self):
        """Drop all columns starting with 'x_studio_' from product_template."""
        table_name = 'project_template'
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
