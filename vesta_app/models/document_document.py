from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class DocumentsDocument(models.Model):
    _inherit = 'documents.document'

    # Updated Category field with the provided selection values
    va_file_category = fields.Selection([
            ('customer_po', 'Customer PO'),
            ('customer_provided', 'Customer Provided'),
            ('vesta_estimate_source_legacy', 'Vesta Estimate Source (Legacy)'),
            ('vesta_estimate_sent_legacy', 'Vesta Estimate Sent (Legacy)'),
            ('project_win_document', 'Project Win Document'),
            ('vendor_estimate', 'Vendor Estimate'),
            ('customer_contract', 'Customer Contract'),
            ('customer_safety_notice', 'Customer Safety Notice'),
        ],
        string='Category',
        store=True
    )

    # Project
    va_file_project = fields.Many2many(
        'project.project',
        string='Project',
        store=True
    )

    # Sales
    va_file_salesorder = fields.Many2many(
        'sale.order',
        string='Sales Order',
        store=True
    )

    def _migrate_studio_fields(self):
        """Perform data migration after module upgrade."""
        # Define field mappings and perform the migration
        field_mappings = {
            'x_studio_file_category': 'va_file_category',
            'x_studio_file_project': 'va_file_project',
            'x_studio_file_salesorder': 'va_file_salesorder',
        }
        for old_field, new_field in field_mappings.items():
            documents = self.env['documents.document'].search([(old_field, '!=', False)])
            for document in documents:
                old_value = getattr(document, old_field, False)
                if old_value:
                    setattr(document, new_field, old_value)
                    # product.save()  # Ensure changes are saved
            _logger.info(f"Migrated {old_field} to {new_field}. Updated {len(document)} records.")

    def _drop_x_studio_columns(self):
        """Drop all columns starting with 'x_studio_' from document_document."""
        table_name = 'documents_document'
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
