from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from attachments.admin import AttachmentInlines

class Slugless(models.Model):
    title = models.CharField(_('Title'), max_length=20)
    
    class Meta:
        verbose_name_plural = _("Sluglesses")

class Sluggish(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=10, unique=True)
    
    class Meta:
        verbose_name_plural = _("Sluggishes")
    
class AttachedAdmin(admin.ModelAdmin):
    inlines=[AttachmentInlines]
    
admin.site.register(Slugless, AttachedAdmin)
admin.site.register(Sluggish, AttachedAdmin)