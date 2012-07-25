from django.db import models
from cms.models import Page
from cms.models.pluginmodel import CMSPlugin
from cms.plugins.picture.models import Picture
from django.utils.translation import ugettext_lazy
import settings
import datetime

class Slide(models.Model):
	image = models.ImageField(ugettext_lazy("image"),upload_to="slides")
	header = models.CharField(max_length=50, blank=True, default = "")
	description = models.CharField(max_length=100, blank=True, default = "")
	start_date = models.DateTimeField(blank=True, null=True, default=None)
	expires = models.DateTimeField(blank=True, null=True, default=None)
	order = models.IntegerField(blank=True, default=50)
	page = models.ForeignKey(Page, blank=True, null=True, default=None)
	link = models.CharField(max_length=200, blank=True, default="")
	
	def __unicode__(self):
		if self.header:
			return self.header[:40]
		elif self.image:
			# added if, because it raised attribute error when file wasn't defined
			try:
				return u"%s" % self.image.path
			except:
				pass
		return "<empty>"
	
class Slideshow(models.Model):
	name = models.CharField(max_length=20)
	show_text_nav = models.BooleanField()
	show_pager_nav = models.BooleanField()
	start_date = models.DateTimeField(blank=True, null=True, default=None)
	expires = models.DateTimeField(blank=True, null=True, default=None)
	slides = models.ManyToManyField(Slide)
	
	def __unicode__(self):
		if self.name:
			return self.name
		return "<empty>"
	
class SlideshowPlugin(CMSPlugin):
	slideshow = models.ForeignKey(Slideshow)
	name = models.CharField(max_length=20)
	
	def __unicode__(self):
		if self.name:
			return self.name
		return "<empty>"

