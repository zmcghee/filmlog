# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entry.rating'
        db.add_column('filmlog_entry', 'rating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.stars'
        db.add_column('filmlog_entry', 'stars',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Entry.date'
        db.alter_column('filmlog_entry', 'date', self.gf('django.db.models.fields.DateField')())
        # Adding field 'Movie.rating'
        db.add_column('filmlog_movie', 'rating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Movie.stars'
        db.add_column('filmlog_movie', 'stars',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Entry.rating'
        db.delete_column('filmlog_entry', 'rating')

        # Deleting field 'Entry.stars'
        db.delete_column('filmlog_entry', 'stars')


        # Changing field 'Entry.date'
        db.alter_column('filmlog_entry', 'date', self.gf('django.db.models.fields.DateField')(auto_now_add=True))
        # Deleting field 'Movie.rating'
        db.delete_column('filmlog_movie', 'rating')

        # Deleting field 'Movie.stars'
        db.delete_column('filmlog_movie', 'stars')


    models = {
        'filmlog.director': {
            'Meta': {'object_name': 'Director'},
            'birth_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'filmlog.entry': {
            'Meta': {'object_name': 'Entry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['filmlog.Movie']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stars': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['filmlog.Venue']"})
        },
        'filmlog.movie': {
            'Meta': {'ordering': "('title_sans_article', 'leading_article', 'premiere_year')", 'object_name': 'Movie'},
            'directors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'movies'", 'symmetrical': 'False', 'to': "orm['filmlog.Director']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.IntegerField', [], {}),
            'leading_article': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'nyc_release_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'premiere_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stars': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'title_sans_article': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'})
        },
        'filmlog.venue': {
            'Meta': {'object_name': 'Venue'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'theatrical': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['filmlog']