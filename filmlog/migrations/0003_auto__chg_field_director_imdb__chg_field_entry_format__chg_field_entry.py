# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Director.imdb'
        db.alter_column('filmlog_director', 'imdb', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Entry.format'
        db.alter_column('filmlog_entry', 'format', self.gf('django.db.models.fields.CharField')(max_length=1, null=True))

        # Changing field 'Entry.venue'
        db.alter_column('filmlog_entry', 'venue_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['filmlog.Venue']))

        # Changing field 'Movie.imdb'
        db.alter_column('filmlog_movie', 'imdb', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Director.imdb'
        raise RuntimeError("Cannot reverse this migration. 'Director.imdb' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Entry.format'
        raise RuntimeError("Cannot reverse this migration. 'Entry.format' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Entry.venue'
        raise RuntimeError("Cannot reverse this migration. 'Entry.venue' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Movie.imdb'
        raise RuntimeError("Cannot reverse this migration. 'Movie.imdb' and its values cannot be restored.")

    models = {
        'filmlog.director': {
            'Meta': {'object_name': 'Director'},
            'birth_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'filmlog.entry': {
            'Meta': {'object_name': 'Entry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['filmlog.Movie']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stars': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
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