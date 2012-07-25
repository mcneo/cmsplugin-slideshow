from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import SlideshowPlugin, Slideshow, Slide
from django.utils.translation import ugettext as _
import datetime

class CMSSlideshowPlugin(CMSPluginBase):
	model = SlideshowPlugin
	name = _("Slideshow")
	render_template = "slideshow.html"

	def render(self, context, instance, placeholder):
		slideshow = ""
		slide_list = []
		filtered_slides = []
		
		slideshow = instance.slideshow
		is_slideshow_available = True # Don't mess with slideshows that are expired
		if slideshow.start_date != None:
			if slideshow.start_date > datetime.datetime.today():
				is_slideshow_available = False
		if slideshow.expires != None:
			if slideshow.expires < datetime.datetime.today():
				is_slideshow_available = False
		if is_slideshow_available:
			slide_list = instance.slideshow.slides.all().order_by('order')
			
			for slide in slide_list:
				is_available = True # Filter out slides that aren't available
				if slide.start_date != None:
					if slide.start_date > datetime.datetime.today():
						is_available = False
				if slide.expires != None:
					if slide.expires < datetime.datetime.today():
						is_available = False
				if is_available:
					new_slide = {}
					new_slide["link"] = ""
					if slide.page != None:
						new_slide["link"] = slide.page.get_absolute_url()
					if new_slide["link"] == "":
						new_slide["link"] = slide.link
					new_slide["image_url"] = slide.image.url
					new_slide["description"] = slide.description
					new_slide["header"] = slide.header
					filtered_slides.append(new_slide)
			
		context.update({
			'slideshow':slideshow,
			'slide_list':filtered_slides,
			'is_slideshow_available':is_slideshow_available
		})
		return context

plugin_pool.register_plugin(CMSSlideshowPlugin)
