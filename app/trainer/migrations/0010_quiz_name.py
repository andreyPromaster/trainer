# Generated by Django 2.2.6 on 2020-05-03 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0009_auto_20200502_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='name', max_length=255),
            preserve_default=False,
        ),
    ]
