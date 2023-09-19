# Generated by Django 4.2.5 on 2023-09-18 08:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_event_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='rating',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(max_length=5000)),
                ('list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.list')),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('tv_episode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.tv_episode')),
                ('tv_series', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.tv_series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]