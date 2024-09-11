# -*- coding: utf-8 -*-
{
    'name': 'Vesta Customizations',
    'version': '17.0.1.0',
    'category': 'Customizations',
    'description': """ Vesta Automation Customizatoins""",
    'author': 'Vesta Automation Inc.',
    'depends': [
        'base',
        'contacts',
        'documents',
        'product',
        'project',
        'sale_management',
        'sales_team',
        'stock',
    ],
    'data': [
        'views/documents_document.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'views/project_project.xml'
    ],
    'pre_init_hook': 'get_studio_fields',
    'post_init_hook': 'post_upgrade_hook',
    'application': True,
    'installable': True,
    'license': 'OPL-1',
}
