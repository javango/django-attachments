from django.views.generic.simple import direct_to_template
from models import Sluggish, Slugless

def index(request, template_name='index.html', extra_context=None):
    """Main view for the testing site"""

    ctx = {
        'sluggish' : Sluggish.objects.all(),
        'slugless' : Slugless.objects.all(),
    }

    if extra_context:
        ctx.update(extra_context)
    return direct_to_template(request, template_name, extra_context=ctx)
