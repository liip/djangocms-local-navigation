# djangocms-local-navigation

This package provides a DjangoCMS plugin that displays a menu based on the
structure of the current page. You can for example create a local menu that is
based on all the h2 elements on your page.

## Installation

`$ pip install djangocms-local-navigation`

Then add it to INSTALLED_APPS:

```
INSTALLED_APPS = (
    # ...
    'djangocms_local_navigation',
)
```

You should now be able to add the plugin "Local menu" to your pages.

## Configuration

### CMS_LOCAL_NAVIGATION_NAV_ELEMENTS

Default: `['h2']`

Defines which elements are used to create the local menu.

### CMS_LOCAL_NAVIGATION_XML_PARSER

Default: `None` (means automatic detection)

Defines which XML parser is used to add anchors to the elements and create the
menu. See
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#specifying-the-parser-to-use
for more information.

## Dependencies

* djangocms-text-ckeditor
