
document.execute('/defaults/application/settings/')

application_name = 'Stickstick'
application_description = 'Share online sticky notes'
application_author = 'Tal Liron'
application_owner = 'Three Crickets'
application_home_url = 'http://threecrickets.com/prudence/stickstick/'
application_contact_email = 'prudence@threecrickets.com'

predefined_globals.update({
    'stickstick.backend': 'h2',
    'stickstick.username': 'root',
    'stickstick.password': 'root',
    'stickstick.host': '',
    'stickstick.database': application_base_path + '/data/stickstick',
    'stickstick.log': document.source.basePath.path + '/logs/stickstick.log'
    })

show_debug_on_error = True
preheat_resources = ['data/']
