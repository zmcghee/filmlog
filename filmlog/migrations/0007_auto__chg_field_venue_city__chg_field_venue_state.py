# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Venue.city'
        db.alter_column('filmlog_venue', 'city', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'Venue.state'
        db.alter_column('filmlog_venue', 'state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Venue.city'
        raise RuntimeError("Cannot reverse this migration. 'Venue.city' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Venue.state'
        raise RuntimeError("Cannot reverse this migration. 'Venue.state' and its values cannot be restored.")

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
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'theatrical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['filmlog']