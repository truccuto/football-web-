# Generated by Django 4.2 on 2023-06-13 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0030_team_stat_awaygoals_alter_result_team1pts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team_stat',
            name='goaldifferencce',
            field=models.IntegerField(default=0),
        ),
    ]
