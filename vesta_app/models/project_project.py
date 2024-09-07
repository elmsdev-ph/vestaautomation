from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    # Anticipated Completion (Legacy)
    va_anticipated_completion = fields.Char(string='Anticipated Completion (Legacy)', store=True)

    # Award Date
    va_award_date = fields.Date(string='Award Date', store=True)

    # Comments (Legacy)
    va_comments_legacy = fields.Char(string='Comments (Legacy)', store=True)

    # CAD
    va_complete_cad = fields.Float(string='CAD', store=True)

    # Electrical
    va_complete_electrical = fields.Float(string='Electrical', store=True)

    # Panel
    va_complete_panel = fields.Float(string='Panel', store=True)

    # Parts Rcvd
    va_complete_parts = fields.Float(string='Parts Rcvd', store=True)

    # Prog
    va_complete_prog = fields.Float(string='Prog', store=True)

    # Completed Date
    va_completed_date = fields.Date(string='Completed Date', store=True)

    # Contract Value
    va_contract_value = fields.Monetary(string='Contract Value', store=True)

    # Cost to Complete
    va_cost_to_complete = fields.Float(string='Cost to Complete', store=True)

    # Customer PO(s)
    va_customer_po = fields.Text(string="Customer PO(s)", store=True)

    # Job ID
    va_job_id = fields.Char(string='Job ID', store=True)

    # Left To Bill
    va_left_to_bill = fields.Float(string='Left To Bill', store=True)

    # Quote (Legacy)
    va_quote_legacy = fields.Text(string='Quote (Legacy)', store=True)

    # Show Design
    va_show_design = fields.Boolean(string='Show Design', store=True)

    # Show Field Install
    va_show_field_install = fields.Boolean(string='Show Field Install', store=True)

    # Show Ordering
    va_show_ordering = fields.Boolean(string='Show Ordering', store=True)

    # Show Panel Build
    va_show_panel_build = fields.Boolean(string='Show Panel Build', store=True)

    # Show Programming
    va_show_programming = fields.Boolean(string='Show Programming', store=True)

    def _migrate_studio_fields(self):
        """Perform data migration after module upgrade."""
        # Define field mappings and perform the migration
        field_mappings = {
            'x_studio_anticipated_completion': 'va_anticipated_completion',
            'x_studio_award_date': 'va_award_date',
            'x_studio_comments_legacy': 'va_comments_legacy',
            'x_studio_complete_cad': 'va_complete_cad',
            'x_studio_complete_electrical': 'va_complete_electrical',
            'x_studio_complete_panel': 'va_complete_panel',
            'x_studio_complete_parts': 'va_complete_parts',
            'x_studio_complete_prog': 'va_complete_prog',
            'x_studio_completed_date': 'va_completed_date',
            'x_studio_contract_value': 'va_contract_value',
            'x_studio_cost_to_complete': 'va_cost_to_complete',
            'x_studio_customer_po': 'va_customer_po',
            'x_studio_job_id': 'va_job_id',
            'x_studio_left_to_bill': 'va_left_to_bill',
            'x_studio_quote_legacy': 'va_quote_legacy',
            'x_studio_show_design': 'va_show_design',
            'x_studio_show_field_install': 'va_show_field_install',
            'x_studio_show_ordering': 'va_show_ordering',
            'x_studio_show_panel_build': 'va_show_panel_build',
            'x_studio_show_programming': 'va_show_programming'
        }
        for old_field, new_field in field_mappings.items():
            projects = self.env['project.project'].search([(old_field, '!=', False)])
            for project in projects:
                old_value = getattr(project, old_field, False)
                if old_value:
                    setattr(project, new_field, old_value)
                    # product.save()  # Ensure changes are saved
            _logger.info(f"Migrated {old_field} to {new_field}. Updated {len(project)} records.")

    def _drop_x_studio_columns(self):
        """Drop all columns starting with 'x_studio_' from project_project."""
        table_name = 'project_project'
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


class ProjectTask(models.Model):
    _inherit = 'project.task'

    va_project_stage = fields.Many2one('project.project.stage', string="Project Stage")

    def _migrate_studio_fields(self):
        """Perform data migration after module upgrade."""
        # Define field mappings and perform the migration
        field_mappings = {
            'x_studio_project_stage': 'va_project_stage',
        }
        for old_field, new_field in field_mappings.items():
            tasks = self.env['project.task'].search([(old_field, '!=', False)])
            for task in tasks:
                old_value = getattr(task, old_field, False)
                if old_value:
                    setattr(task, new_field, old_value)
                    # product.save()  # Ensure changes are saved
            _logger.info(f"Migrated {old_field} to {new_field}. Updated {len(task)} records.")

    def _drop_x_studio_columns(self):
        """Drop all columns starting with 'x_studio_' from project_task."""
        table_name = 'project_task'
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
