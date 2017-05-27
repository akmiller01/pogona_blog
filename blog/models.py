from django.db import models
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailsearch import index

from wagtail.wagtailsnippets.models import register_snippet

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django import forms
from django.forms import ModelForm
from django.shortcuts import render, redirect

from django.utils import formats

from ipware.ip import get_real_ip

class BlogIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage']
    
    content_panels = [
        FieldPanel('title', classname="full title"),
    ]   

    promote_panels = Page.promote_panels
    
    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blogs = blogs.order_by('-date')

        return blogs

    def get_context(self, request):
        # Get blogs
        blogs = self.blogs

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)
            
        # Filter by category
        category = request.GET.get('category')
        if category:
            blogs = blogs.filter(categories__name=category)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(blogs, 5)  # Show 10 blogs per page
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')

class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"
        
class EndNoteBlock(StructBlock):
    number = CharBlock()
    citation = CharBlock()
        
class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"
        
class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()

class BlogStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    endnote = EndNoteBlock()
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")

class BlogPage(Page):
    date = models.DateField("Post date")
    body = StreamField(BlogStreamBlock())
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []
    
    @property
    def comments(self):
        # Get list of live blog pages that are descendants of this page
        comments = self.blog_comments.filter(approved=True).order_by('created')

        return comments
    
    @property
    def comment_count(self):
        # Get list of live blog pages that are descendants of this page
        comments = self.blog_comments.filter(approved=True).count()

        return comments
    
    @property
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
        
    @property
    def category_concat(self):
        categories = self.categories.values_list('name', flat=True) 
        return " ".join(categories)
    
    @property
    def tag_concat(self):
        tags = self.tags.values_list('name', flat=True) 
        return " ".join(tags)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('category_concat'),
        index.SearchField('tag_concat')
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        StreamFieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    
    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
    ]
    
    comment_panels = [InlinePanel('blog_comments', label="Comments")]
    
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(comment_panels, heading='Comments'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
    
    @property
    def blog_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()
    
    def serve(self, request):
        
        context = super(BlogPage, self).get_context(request)

        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                if not comment.name:
                    comment.name = "anonymous"
                comment.page_id = self.id
                comment.approved = False
                comment.post_as_administrator = False
                comment.ip_address = get_real_ip(request)
                comment.save()
                return redirect(self.url)
        else:
            form = CommentForm()
        
        context['page'] = self
        context['form'] = form
        context['comments'] = self.comments
        context['comment_count'] = self.comment_count
        
        return render(request, self.template, context)

    
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
    
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'
        
class AboutPage(Page):
    body = StreamField(BlogStreamBlock())
    parent_page_types = ['home.HomePage']
    subpage_types = []
    
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
    
class Comment(models.Model):
    name = models.CharField(max_length=255,blank=True,help_text="(optional)")
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    approved = models.BooleanField(default=False)
    post_as_administrator = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True,null=True)

    class Meta:
        abstract = True
        ordering = ['approved','-created']

@register_snippet
class BlogPageComment(Orderable,Comment):
    page = ParentalKey(BlogPage,related_name='blog_comments')
    
    def __str__(self):
        if self.approved:
            return "Approved comment by "+self.name+" on "+formats.date_format(self.created,'F j, Y @ f a')
        else:
            return "Unapproved comment by "+self.name+" on "+formats.date_format(self.created,'F j, Y @ f a')
        
    class Meta:
        ordering = ['approved','-created']

class CommentForm(ModelForm):
    class Meta:
        model = BlogPageComment
        fields = ['name','comment']
        
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'comment':forms.Textarea(attrs={"class":"form-control","rows":4}),
        }