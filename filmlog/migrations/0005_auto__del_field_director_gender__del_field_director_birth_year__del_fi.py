# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Director.gender'
        db.delete_column('filmlog_director', 'gender')

        # Deleting field 'Director.birth_year'
        db.delete_column('filmlog_director', 'birth_year')

        # Deleting field 'Entry.rating'
        db.delete_column('filmlog_entry', 'rating')

        # Deleting field 'Entry.stars'
        db.delete_column('filmlog_entry', 'stars')

        # Adding field 'Entry.in_3d'
        db.add_column('filmlog_entry', 'in_3d',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Entry.notes'
        db.add_column('filmlog_entry', 'notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Venue.website'
        db.add_column('filmlog_venue', 'website',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Movie.rating'
        db.delete_column('filmlog_movie', 'rating')

        # Deleting field 'Movie.stars'
        db.delete_column('filmlog_movie', 'stars')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Director.gender'
        raise RuntimeError("Cannot reverse this migration. 'Director.gender' and its values cannot be restored.")
        # Adding field 'Director.birth_year'
        db.add_column('filmlog_director', 'birth_year',
                      self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.rating'
        db.add_column('filmlog_entry', 'rating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.stars'
        db.add_column('filmlog_entry', 'stars',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Entry.in_3d'
        db.delete_column('filmlog_entry', 'in_3d')

        # Deleting field 'Entry.notes'
        db.delete_column('filmlog_entry', 'notes')

        # Deleting field 'Venue.website'
        db.delete_column('filmlog_venue', 'website')

        # Adding field 'Movie.rating'
        db.add_column('filmlog_movie', 'rating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Movie.stars'
        db.add_column('filmlog_movie', 'stars',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)


    models = {
        'filmlog.director': {
            'Meta': {'object_name': 'Director'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'filmlog.entry': {
            'Meta': {'object_name': 'Entry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_3d': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['filmlog.Movie']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'repeat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entries'", 'null': 'True', 'to': "orm['filmlog.Venue']"})
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
            'Meta': {'object_name': 'Venue'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'theatrical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['filmlog']