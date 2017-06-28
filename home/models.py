from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from blog.models import BlogStreamBlock


class HomePage(Page):
    header = models.CharField(max_length=250,blank=True)
    motto = models.CharField(max_length=250,blank=True)
    parent_page_types = ['wagtailcore.Page']
    
    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(HomePage, cls).can_create_at(parent) \
            and not cls.objects.exists()
    
    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('motto'),
    ]
