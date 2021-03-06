# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entry.walkout'
        db.add_column('filmlog_entry', 'walkout',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Entry.walkout'
        db.delete_column('filmlog_entry', 'walkout')


    models = {
        'filmlog.director': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Director'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'filmlog.entry': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'Entry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_3d': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['filmlog.Movie']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'repeat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entries'", 'null': 'True', 'to': "orm['filmlog.Venue']"}),
            'walkout': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'filmlog.movie': {
            'Meta': {'ordering': "('title_sans_article', 'leading_article', 'premiere_year')", 'object_name': 'Movie'},
            'directors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'movies'", 'symmetrical': 'False', 'to': "orm['filmlog.Director']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'leading_article': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'nyc_release_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'premiere_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'title_sans_article': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'})
        },
        'filmlog.venue': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Venue'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'theatrical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['filmlog']