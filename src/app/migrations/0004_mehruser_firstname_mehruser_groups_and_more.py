# Generated by Django 4.2.9 on 2024-02-20 12:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0003_remove_mehruser_help_history_alter_charityhelp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='mehruser',
            name='firstName',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='lastName',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='password',
            field=models.CharField(default='s', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mehruser',
            name='profilePhoto',
            field=models.ImageField(blank=True, null=True, upload_to='app/images'),
        ),
        migrations.AddField(
            model_name='mehruser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='charityhelp',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 2, 20, 15, 37, 6, 385857)),
        ),
        migrations.AlterField(
            model_name='institute',
            name='logo',
            field=models.ImageField(upload_to='app/Logos'),
        ),
        migrations.AlterField(
            model_name='mehruser',
            name='phone',
            field=models.CharField(max_length=11, unique=True),
        ),
        migrations.CreateModel(
            name='OtpUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField(default=12345, max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]