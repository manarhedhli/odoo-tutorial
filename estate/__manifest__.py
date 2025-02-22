{
    'name': 'ESTATE',
    'depends': [
        'base',
        'account',
        'contacts'
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/inherited_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
