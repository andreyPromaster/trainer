# Generated by Django 2.2.6 on 2020-05-11 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0010_quiz_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='taken_quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='taken_quiz_answers', to='trainer.TakenQuiz'),
            preserve_default=False,
        ),
    ]
