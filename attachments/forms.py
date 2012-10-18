from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from attachments.models import Attachment
from django.conf import settings

ATTACHMENT_FIELDS = getattr(settings, 'ATTACHMENT_FIELDS', ('attachment_file', 'mime_type'))
class AttachmentForm(forms.ModelForm):
    attachment_file = forms.FileField(label=_('Upload attachment'))

    class Meta:
        model = Attachment
        fields = ATTACHMENT_FIELDS

    def save(self, request, obj, *args, **kwargs):
        self.instance.creator = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.id
        super(AttachmentForm, self).save(*args, **kwargs)