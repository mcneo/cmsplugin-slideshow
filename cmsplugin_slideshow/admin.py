from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdmin
from models import Slideshow, Slide
from cms.plugins.picture.models import Picture
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a> %s ' % \
                (image_url, image_url, file_name, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
	
class SlideshowAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_text_nav', 'show_pager_nav', 'start_date', 'expires')
    filter_horizontal = ("slides",)
    
class SlideAdmin(admin.ModelAdmin):
    list_display = ('image','order', 'header', 'description', 'start_date', 'expires')
    list_editable = ('header','description','order',)
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(SlideAdmin,self).formfield_for_dbfield(db_field, **kwargs)
        
admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Slide, SlideAdmin)
