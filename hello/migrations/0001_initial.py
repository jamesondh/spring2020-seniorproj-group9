# Generated by Django 3.0.3 on 2020-02-15 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_text', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('completed_date', models.DateTimeField(blank=True, verbose_name='date completed')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='Job_Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentiment_score', models.FloatField()),
                ('executed_date', models.DateTimeField(blank=True, verbose_name='date executed')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.Jobs')),
            ],
        ),
    ]
