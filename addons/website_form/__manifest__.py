{
    'name': 'Website Form',
    'category': 'Website/Website',
    'summary': 'Build custom web forms',
    'description': """
        Customize and create your own web forms.
        This module adds a new building block in the website builder in order to build new forms from scratch in any website page.
    """,
    'version': '1.0',
    'depends': ['website', 'mail', 'google_recaptcha'],
    'data': [
        'data/mail_mail_data.xml',
        'views/assets.xml',
        'views/ir_model_views.xml',
        'views/snippets/snippets.xml',
        'views/snippets/s_website_form.xml',
        'views/website_form_templates.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
