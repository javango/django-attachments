import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

class AttachmentManager(models.Manager):
    def attachments_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)

class Attachment(models.Model):
    @staticmethod
    def attachment_upload(instance, filename):
        """Stores the attachment in a "per module/appname/object_id" folder"""
        content_object = instance.content_object
        try:
            object_id = content_object.slug
        except AttributeError:
            object_id = content_object.pk

        return 'attachments/%s/%s/%s' % (
            '%s_%s' % (content_object._meta.app_label,
                       content_object._meta.object_name.lower()),
                       object_id,
                       filename)

    objects = AttachmentManager()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(User, related_name="created_attachments", verbose_name=_('creator'))
    attachment_file = models.FileField(_('attachment'), upload_to=attachment_upload)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    safe = models.BooleanField (_('safe'), default=False)
    mime_type = models.CharField(_('mime_type'), max_length=50, null=True, blank=True,
                                 help_text=_('leave empty to handle by file extension'))


    class Meta:
        ordering = ['-created']
        permissions = (
            ('delete_foreign_attachments', 'Can delete foreign attachments'),
        )

    def __unicode__(self):
        return '%s attached %s' % (self.creator.username, self.attachment_file.name)

    @property
    def filename(self):
        return os.path.split(self.attachment_file.name)[1]