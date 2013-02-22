==================
django-attachments
==================

django-attachments is a generic set of template tags to attach any kind of
files to models.

Installation:
=============

1. Put ``attachments`` to your ``INSTALLED_APPS`` in your ``settings.py``
   within your django project.

2. Add ``(r'^attachments/', include('attachments.urls')),`` to your ``urls.py``.

3. Add ``'django.core.context_processors.request'`` to your ``TEMPLATE_CONTEXT_PROCESSORS``
   in your settings.py. If this setting does not exist, simply add the following
   snippet at the end of your settings.py::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.request',
    )

4. Don't forget to resync your database::

    ./manage.py syncdb

5. If you are upgrading from a previous version, you may wish to migrate your
   database using ``south`` ::

    ./manage.py migrate attachments

   you may need to fake the first migration::

    ./manage.py migrate attachments 0001 --fake
    ./manage.py migrate attachments

6. Grant the user some permissons:

   * For **adding attachments** grant the user (or group) the permission
     ``attachments.add_attachments``.

   * For **deleting attachments** grant the user (or group) the permission
     ``attachments.delete_attachments``. This allows the user to delete only
     attachments which are assigned to him (rather the attachments he uploaded self).

   * For **deleting foreign attachments** (attachments by other users) grant
     the user the permission ``attachments.delete_foreign_attachments``.
     
   This only works for the templatetags, the admin still allows anybody to add
   or delete attachments.

7. (optional) customise the storage object to store files in a location other
   than in ``MEDIA_ROOT`` or serve from a url other than ``MEDIA_URL``. You may
   customise the storage object which is used on the FileField. To do this,
   simply define the following setting in your ``settings.py``::
     
     ATTACHMENTS_STORAGE

   The ``ATTACHMENTS_STORAGE`` should be set to an instance of a storage object that you 
   would like to use instead of the default DefaultStorage object. An example
   which stores files in a secure location may look like this:: 

     from django.core.files.storage import FileSystemStorage
     ATTACHMENTS_ROOT = '/path/to/my/secure/location'
     ATTACHMENTS_URL = '/secure'
     ATTACHMENTS_STORAGE = FileSystemStorage(
                                        location=ATTACHMENTS_ROOT,
                                        base_url=ATTACHMENTS_URL)

   Note that you **must** define both ``location`` and ``base_url`` for this to work.
   Otherwise django will attempt to load the settings file again to find the
   ``settings.MEDIA_ROOT`` or ``settings.MEDIA_URL`` defaults, crashing django. 


Mind that you serve files!
==========================

django-attachments stores the files in your site_media directory and does not modify
them. For example, if an user uploads a .html file your webserver will probably display
it in HTML. It's a good idea to serve such files as plain text. In a Apache2
configuration this would look like:: 

    <Location /site_media/attachments>
        AddType text/plain .html .htm .shtml .php .php5 .php4 .pl .cgi
    </Location>


Usage:
======

In contrib.admin:
-----------------

django-attachments provides a inline object to add a list of attachments to
any kind of model in your admin app.

Simply add ``AttachmentInlines`` to the admin options of your model. Example::

    from django.contrib import admin
    from attachments.admin import AttachmentInlines

    class MyEntryOptions(admin.ModelAdmin):
        inlines = [AttachmentInlines]

.. image:: http://cloud.github.com/downloads/bartTC/django-attachments/attachments_screenshot_admin.png

In your frontend templates:
---------------------------

First of all, load the attachments_tags in every template you want to use it::

    {% load attachments_tags %}
    
django-attachments comes with some templatetags to add or delete attachments
for your model objects in your frontend.

1. ``get_attachments_for [object]``: Fetches the attachments for the given
   model instance. You can optionally define a variable name in which the attachment
   list is stored in the template context. The default context variable name is
   ``attachments`` Example::
   
   {% get_attachments_for entry as "attachments_list" %}

2. ``attachment_form``: Renders a upload form to add attachments for the given
   model instance. Example::
   
    {% attachment_form [object] %}

   It returns an empty string if the current user is not logged in.

3. ``attachment_delete_link``: Renders a link to the delete view for the given
   *attachment*. Example::
   
    {% for att in attachments_list %}
        {{ att }} {% attachment_delete_link att %}
    {% endfor %}
    
   This tag automatically checks for permission. It returns only a html link if the
   give n attachment's creator is the current logged in user or the user has the 
   ``delete_foreign_attachments`` permission.

Quick Example:
==============

::

    {% load attachments_tags %}
    {% get_attachments_for entry as "my_entry_attachments" %}
    
    {% if my_entry_attachments %}
    <ul>
    {% for attachment in my_entry_attachments %}
        <li>
            <a href="{{ attachment.attachment_file.url }}">{{ attachment.link_name }}</a>
            {% attachment_delete_link attachment %}
        </li>
    {% endfor %}
    </ul>
    {% endif %}

    {% attachment_form entry %}

In the console:
===============

First, import the items you will need::

    import os
    from django.core.files import File
    from attachments.models import Attachment
    from myproject.models import Person

Next, retrieve the object you wish to attach to::

    me = Person.objects.get(name='aaron')

Now open the attachment you want from your drive using the django File object::

    mypicture = File(open('/home/aaron/mypicture.jpg', 'r'))

Finally, create the Attachment object and save it, and close the file handle::

    a = Attachment()
    a.creator = me
    a.attachment_file = mypicture
    a.save()
    mypicture.close()

Changelog:
==========

v0.4.2 (2013-02-22):

   * Change the json content_type to text/plain to work with ie8 and other ie versions.  When using jquery setting
     dataType to 'json' will treat the response as json even with the 'broken' content_type
   
   * Workaround for ajax uploads using jquery.form for browsers that don't support XMLHttpRequest level 2.
     Add isajaxrequest to the data submitted in the POST
       
       var options = {'data': { isajaxrequest: 'true' } };
       $('#myform).').ajaxForm(options);
     
v0.4.1 (2012-10-18):

    * Addeed support for json/ajax in the add/delete views.

      The add_attachment and delete_attachment views will return a json response if called via ajax/json.

      Sample json responses after successfuly upload::

       messages: [{message:"Your attachment was deleted.", title:"Success"}]

      Sample json response after failed upload::

       form_html: "<the html to re-display>"
       messages: [{message:"Please correct the form errors.", title:"Error"}]
       
v0.4 (2011-04-4):
 
    * Added a new field display_name to the Attachments model. South migrations have been
      provided to help with the transition to using the new field. 

      why add display_name?
      Previously it wasn't practical to set a nice display name for attachment links.
      The best we could do was attachment.filename. Now our link text can be whatever we like::

       <a href="/myatt4c_hm3nt_badfilename.pdf">2011 yearly report</a>

      from this template::

       <a href="{{ attachment.attachment_file.url }}">{{ attachment.link_name }}</a>

      where link_name is a convenience function that tries to return display_name if it exists.
      if not it will return filename.

v0.3.1 (2009-07-29):

    * Added a note to the README that you should secure your static files.

v0.3 (2009-07-22):

    * This version adds more granular control about user permissons. You need
      to explicitly add permissions to users who should been able to upload,
      delete or delete foreign attachments. 

      This might be **backwards incompatible** as you did not need to assign add/delete
      permissions before!
