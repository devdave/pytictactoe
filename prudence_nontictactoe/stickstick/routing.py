
document.execute('/defaults/application/routing/')

from com.threecrickets.prudence.util import CssUnifyMinifyFilter, JavaScriptUnifyMinifyFilter

router.captureAndHide(resources_base_url + 'data/note/{id}/', '/data/note/')

# Wrap the static web with unify-minify filters
css_filter = CssUnifyMinifyFilter(None, File(application_base_path + static_web_base_path), minimum_time_between_validity_checks)
java_script_filter = JavaScriptUnifyMinifyFilter(None, File(application_base_path + static_web_base_path), minimum_time_between_validity_checks)
router.filterBase(static_web_base_url, css_filter, static_web)
router.filterBase(static_web_base_url, java_script_filter, css_filter)
