from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django.conf import settings
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes
from wagtail.wagtailadmin.rich_text import HalloPlugin
from django.conf.urls.static import static
#  
# def whitelister_element_rules():
#     return {
#         'a': attribute_rule({'href': check_url, 'target': True}),
#         'blockquote': attribute_rule({'class': True}),
#     }
# hooks.register('construct_whitelister_element_rules', whitelister_element_rules)
 
def register_custom_buttons(features):
    features.register_editor_plugin(
        'hallo', 'superscriptformat',
        HalloPlugin(
            name='superscriptformat',
            js=[static('js/hallo-custombuttons.js')],
        )
    )
    features.default_features.append('superscriptformat')
    features.register_editor_plugin(
        'hallo', 'endnoteanchorbutton',
        HalloPlugin(
            name='endnoteanchorbutton',
            js=[static('js/hallo-custombuttons.js')],
        )
    )
    features.default_features.append('endnoteanchorbutton')
hooks.register('register_rich_text_feature',register_custom_buttons)
def editor_js():
    js_files = [
        'js/hallo-custombuttons.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
 
    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('superscriptformat');
            registerHalloPlugin('endnoteanchorbutton');
        </script>
        """
    )
 
hooks.register('insert_editor_js', editor_js)
 
def editor_css():
    return format_html('<link rel="stylesheet" href="'+ settings.STATIC_URL + 'css/font-awesome.min.css">')
 
hooks.register('insert_editor_css', editor_css)
