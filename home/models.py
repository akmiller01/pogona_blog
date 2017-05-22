from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from blog.models import BlogStreamBlock


class HomePage(Page):
    body = StreamField(BlogStreamBlock())
    parent_page_types = ['wagtailcore.Page']
    
    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(HomePage, cls).can_create_at(parent) \
            and not cls.objects.exists()
    
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
