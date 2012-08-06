# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CatalogEntry.slug'
        db.add_column('ecm_catalogentry', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CatalogEntry.slug'
        db.delete_column('ecm_catalogentry', 'slug')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ecm.article': {
            'Meta': {'object_name': 'Article', '_ormbases': ['ecm.CatalogEntry']},
            'catalogentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ecm.CatalogEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '255'})
        },
        'ecm.catalogentry': {
            'Meta': {'object_name': 'CatalogEntry'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['ecm.CatalogEntry']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'ecm.folder': {
            'Meta': {'object_name': 'Folder', '_ormbases': ['ecm.CatalogEntry']},
            'catalogentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ecm.CatalogEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ecm.site': {
            'Meta': {'object_name': 'Site', '_ormbases': ['ecm.CatalogEntry']},
            'catalogentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ecm.CatalogEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['ecm']