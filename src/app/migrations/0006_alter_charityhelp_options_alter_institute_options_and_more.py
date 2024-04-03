# Generated by Django 4.1 on 2024-02-21 11:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_project_logo_alter_charityhelp_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charityhelp',
            options={'verbose_name': 'کمک', 'verbose_name_plural': 'کمک ها'},
        ),
        migrations.AlterModelOptions(
            name='institute',
            options={'verbose_name': 'موسسه', 'verbose_name_plural': 'موسسه ها'},
        ),
        migrations.AlterModelOptions(
            name='mehruser',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'پروژه', 'verbose_name_plural': 'پروژه ها'},
        ),
        migrations.AlterField(
            model_name='charityhelp',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 15, 6, 20, 499794)),
        ),
        migrations.AlterField(
            model_name='charityhelp',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project'),
        ),
        migrations.AlterField(
            model_name='charityhelp',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='institute',
            name='logo',
            field=models.ImageField(upload_to='admin-interface/institute_logos'),
        ),
        migrations.AlterField(
            model_name='mehruser',
            name='profilePhoto',
            field=models.ImageField(blank=True, null=True, upload_to='admin-interface/images'),
        ),
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='admin-interface/project_logos'),
        ),
    ]
