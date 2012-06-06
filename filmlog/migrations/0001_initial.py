# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Director'
        db.create_table('filmlog_director', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('imdb', self.gf('django.db.models.fields.IntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('birth_year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal('filmlog', ['Director'])

        # Adding model 'Movie'
        db.create_table('filmlog_movie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title_sans_article', self.gf('django.db.models.fields.CharField')(max_length=250, db_index=True)),
            ('leading_article', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('imdb', self.gf('django.db.models.fields.IntegerField')()),
            ('premiere_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('nyc_release_year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal('filmlog', ['Movie'])

        # Adding M2M table for field directors on 'Movie'
        db.create_table('filmlog_movie_directors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['filmlog.movie'], null=False)),
            ('director', models.ForeignKey(orm['filmlog.director'], null=False))
        ))
        db.create_unique('filmlog_movie_directors', ['movie_id', 'director_id'])

        # Adding model 'Venue'
        db.create_table('filmlog_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('theatrical', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('filmlog', ['Venue'])

        # Adding model 'Entry'
        db.create_table('filmlog_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['filmlog.Movie'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['filmlog.Venue'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('filmlog', ['Entry'])


    def backwards(self, orm):
        # Deleting model 'Director'
        db.delete_table('filmlog_director')

        # Deleting model 'Movie'
        db.delete_table('filmlog_movie')

        # Removing M2M table for field directors on 'Movie'
        db.delete_table('filmlog_movie_directors')

        # Deleting model 'Venue'
        db.delete_table('filmlog_venue')

        # Deleting model 'Entry'
        db.delete_table('filmlog_entry')


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
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['filmlog.Movie']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['filmlog.Venue']"})
        },
        'filmlog.movie': {
            'Meta': {'object_name': 'Movie'},
            'directors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'movies'", 'symmetrical': 'False', 'to': "orm['filmlog.Director']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.IntegerField', [], {}),
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
            'theatrical': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['filmlog']