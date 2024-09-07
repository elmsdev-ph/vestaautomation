from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # New File
    va_binary_field_1q6_1h7gdnota = fields.Binary(string='New File')

    # Filename for va_binary_field_1q6_1h7gdnota
    va_binary_field_1q6_1h7gdnota_filename = fields.Char(string='Filename for New File')

    # New Text Fields
    va_char_field_486_1h95oftjn = fields.Char(string='New Text')
    va_char_field_4km_1h7gc0o8n = fields.Char(string='New Text')
    va_char_field_5vj_1h7gc47a6 = fields.Char(string='New Text')
    va_char_field_60g_1h7gcc5im = fields.Char(string='New Text')
    va_char_field_66q_1h7gcb2om = fields.Char(string='New Text')
    va_char_field_om_1h93mu83u = fields.Char(string='New Text')

    # Cut Sheet
    va_cut_sheet = fields.Binary(string='Cut Sheet')

    # Filename for va_cut_sheet
    va_cut_sheet_filename = fields.Char(string='Filename for Cut Sheet')

    # Additional Notes
    va_description = fields.Char(string='Additional Notes')

    # MFR Code
    va_mfr_code = fields.Char(string='MFR Code')

    # MFR Number
    va_mfr_number = fields.Char(string='MFR Number')

    # Preferred Vendor (Selection field)
    va_preferred_vendor = fields.Selection([
        ('vendor1', 'Vendor 1'),
        ('vendor2', 'Vendor 2'),
        ('vendor3', 'Vendor 3')
    ], string='Preferred Vendor')

    # Product Code
    va_product_code = fields.Char(string='Product Code')

    # New Related Field (Many2one to product.product)
    va_related_field_20v_1hcvakv6c = fields.Many2one('product.product', string='New Related Field')

    # New Selection (Selection field)
    va_selection_field_51i_1hcvag7qt = fields.Selection([
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3')
    ], string='New Selection')

    # Supplier's Code
    va_suppliers_code = fields.Char(string="Supplier's Code")

    # Supplier's Webpage
    va_suppliers_webpage = fields.Char(string="Supplier's Webpage")

    def _migrate_studio_fields(self):
        """Perform data migration after module upgrade."""
        # Define field mappings and perform the migration
        field_mappings = {
            'x_studio_binary_field_1q6_1h7gdnota': 'va_binary_field_1q6_1h7gdnota',
            'x_studio_binary_field_1q6_1h7gdnota_filename': 'va_binary_field_1q6_1h7gdnota_filename',
            'x_studio_char_field_486_1h95oftjn': 'va_char_field_486_1h95oftjn',
            'x_studio_char_field_4km_1h7gc0o8n': 'va_char_field_4km_1h7gc0o8n',
            'x_studio_char_field_5vj_1h7gc47a6': 'va_char_field_5vj_1h7gc47a6',
            'x_studio_char_field_60g_1h7gcc5im': 'va_char_field_60g_1h7gcc5im',
            'x_studio_char_field_66q_1h7gcb2om': 'va_char_field_66q_1h7gcb2om',
            'x_studio_char_field_om_1h93mu83u': 'va_char_field_om_1h93mu83u',
            'x_studio_cut_sheet': 'va_cut_sheet',
            'x_studio_cut_sheet_filename': 'va_cut_sheet_filename',
            'x_studio_description': 'va_description',
            'x_studio_mfr_code': 'va_mfr_code',
            'x_studio_mfr_number': 'va_mfr_number',
            'x_studio_preferred_vendor': 'va_preferred_vendor',
            'x_studio_product_code': 'va_product_code',
            'x_studio_related_field_20v_1hcvakv6c': 'va_related_field_20v_1hcvakv6c',
            'x_studio_selection_field_51i_1hcvag7qt': 'va_selection_field_51i_1hcvag7qt',
            'x_studio_suppliers_code': 'va_suppliers_code',
            'x_studio_suppliers_webpage': 'va_suppliers_webpage',
        }
        for old_field, new_field in field_mappings.items():
            products = self.env['product.product'].search([(old_field, '!=', False)])
            for product in products:
                old_value = getattr(product, old_field, False)
                if old_value:
                    setattr(product, new_field, old_value)
                    # product.save()  # Ensure changes are saved
            _logger.info(f"Migrated {old_field} to {new_field}. Updated {len(products)} records.")

    def _drop_x_studio_columns(self):
        """Drop all columns starting with 'x_studio_' from product_product."""
        table_name = 'product_product'
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
