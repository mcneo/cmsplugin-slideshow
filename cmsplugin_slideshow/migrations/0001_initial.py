# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Slide'
        db.create_table('slideshow_slide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires', self.gf('django.db.models.fields.DateTimeField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('slideshow', ['Slide'])

        # Adding model 'SlidshowPlugin'
        db.create_table('cmsplugin_slidshowplugin', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('show_text_nav', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_pager_nav', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('slideshow', ['SlidshowPlugin'])

        # Adding M2M table for field slides on 'SlidshowPlugin'
        db.create_table('slideshow_slidshowplugin_slides', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('slidshowplugin', models.ForeignKey(orm['slideshow.slidshowplugin'], null=False)),
            ('slide', models.ForeignKey(orm['slideshow.slide'], null=False))
        ))
        db.create_unique('slideshow_slidshowplugin_slides', ['slidshowplugin_id', 'slide_id'])


    def backwards(self, orm):
        
        # Deleting model 'Slide'
        db.delete_table('slideshow_slide')

        # Deleting model 'SlidshowPlugin'
        db.delete_table('cmsplugin_slidshowplugin')

        # Removing M2M table for field slides on 'SlidshowPlugin'
        db.delete_table('slideshow_slidshowplugin_slides')


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
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'slideshow.slide': {
            'Meta': {'object_name': 'Slide'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'slideshow.slidshowplugin': {
            'Meta': {'object_name': 'SlidshowPlugin', 'db_table': "'cmsplugin_slidshowplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'show_pager_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_text_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slides': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['slideshow.Slide']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['slideshow']
