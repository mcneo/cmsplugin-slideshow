# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		
		# Complete all the Changes to the columns of the slide table
		db.delete_column('slideshow_slide', 'header')
		db.delete_column('slideshow_slide', 'description')
		db.delete_column('slideshow_slide', 'start_date')
		db.delete_column('slideshow_slide', 'expires')
		db.delete_column('slideshow_slide', 'order')
		db.add_column('slideshow_slide', 'header', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=True)
		db.add_column('slideshow_slide', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=True)
		db.add_column('slideshow_slide', 'start_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True), keep_default=True)
		db.add_column('slideshow_slide', 'expires', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True), keep_default=True)
		db.add_column('slideshow_slide', 'page', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['cms.Page'], null=True), keep_default=True)
		db.add_column('slideshow_slide', 'link', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=True)
		db.add_column('slideshow_slide', 'order', self.gf('django.db.models.fields.IntegerField')(default=50), keep_default=True)
		
		#Create the Slideshow Table
		db.create_table('slideshow_slideshow', (
			('id', models.AutoField(primary_key=True)),
		))
		db.send_create_signal('slideshow', ['Slideshow'])  
		db.add_column('slideshow_slideshow', 'name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))
		db.add_column('slideshow_slideshow', 'show_text_nav', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=True)
		db.add_column('slideshow_slideshow', 'show_pager_nav', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=True)
		db.add_column('slideshow_slideshow', 'start_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True), keep_default=True)
		db.add_column('slideshow_slideshow', 'expires', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True), keep_default=True)
		
		#Make the changes to the slideshow_slideshow_slides Many 2 Many Table
		db.rename_table('slideshow_slidshowplugin_slides', 'slideshow_slideshow_slides')
		db.rename_column('slideshow_slideshow_slides', 'slidshowplugin_id', 'slideshow_id')
		
		# Fix the Plugins Table
		db.rename_table('cmsplugin_slidshowplugin', 'cmsplugin_slideshowplugin')
		db.add_column('cmsplugin_slideshowplugin', 'slideshow', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['slideshow.Slideshow']))
		
		#Link up the new slideshow Table with the slideshow data from cmsplugins
		if not db.dry_run:
			slideshows = orm.SlideshowPlugin.objects.raw('SELECT cmsplugin_ptr_id, name from cmsplugin_slideshowplugin')
			for a_slideshow in slideshows:
				db.execute("INSERT slideshow_slideshow SET id=%s, name=%s, show_text_nav=0, show_pager_nav=0, start_date=NULL, expires=NULL", [a_slideshow.pk, a_slideshow.name])
				raw_string = "SELECT id FROM slideshow_slideshow WHERE name='%s'" % a_slideshow.name
				show_id = orm.Slideshow.objects.raw(raw_string)[0].pk
				raw_string = "UPDATE cmsplugin_slideshowplugin SET slideshow_id=%s WHERE name='%s'" % (show_id, a_slideshow.name)
				db.execute(raw_string)
		
		db.create_unique('slideshow_slideshow', ['id'])
		
		db.delete_column('cmsplugin_slideshowplugin', 'show_text_nav')
		db.delete_column('cmsplugin_slideshowplugin', 'show_pager_nav')
		db.delete_column('cmsplugin_slideshowplugin', 'start_date')
		db.delete_column('cmsplugin_slideshowplugin', 'expires')

	def backwards(self, orm):
		raise RuntimeError("Cannot reverse this migration.")


	models = {
		'cms.cmsplugin': {
			'Meta': {'object_name': 'CMSPlugin'},
			'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
			'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
			'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
			'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
			'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
			'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
			'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
			'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
			'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
		},
		'cms.page': {
			'Meta': {'ordering': "('site', 'tree_id', 'lft')", 'object_name': 'Page'},
			'changed_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
			'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
			'created_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
			'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
			'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
			'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
			'limit_visibility_in_menu': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
			'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'moderator_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'blank': 'True'}),
			'navigation_extenders': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '80', 'null': 'True', 'blank': 'True'}),
			'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cms.Page']"}),
			'placeholders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cms.Placeholder']", 'symmetrical': 'False'}),
			'publication_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
			'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
			'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
			'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.Page']"}),
			'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
			'reverse_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
			'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
			'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
			'soft_root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
			'template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
		},
		'cms.placeholder': {
			'Meta': {'object_name': 'Placeholder'},
			'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
		},
		'sites.site': {
			'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
			'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
		},
		'slideshow.slide': {
			'Meta': {'object_name': 'Slide'},
			'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
			'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 3, 17, 58, 40, 943656)'}),
			'header': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
			'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
			'order': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
			'page': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['cms.Page']", 'null': 'True'}),
			'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 3, 17, 58, 40, 943525)'})
		},
		'slideshow.slideshow': {
			'Meta': {'object_name': 'Slideshow'},
			'expires': ('django.db.models.fields.DateTimeField', [], {}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
			'show_pager_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'show_text_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'slides': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['slideshow.Slide']", 'symmetrical': 'False'}),
			'start_date': ('django.db.models.fields.DateTimeField', [], {})
		},
		'slideshow.slideshowplugin': {
			'Meta': {'object_name': 'SlideshowPlugin', 'db_table': "'cmsplugin_slideshowplugin'", '_ormbases': ['cms.CMSPlugin']},
			'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
			'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['slideshow.Slideshow']"})
		}
	}

	complete_apps = ['slideshow']
