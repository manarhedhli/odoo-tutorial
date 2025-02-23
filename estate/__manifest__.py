{
    'name': 'ESTATE',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base',
        'account',
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'reports/estate_property_reports.xml',
        'reports/estate_property_offer_templates.xml',
        'reports/estate_property_templates.xml',
        'reports/res_users_templates.xml',

        'views/inherited_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate.property.type.csv',
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
