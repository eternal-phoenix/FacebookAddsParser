# Generated by Django 4.2.2 on 2023-06-10 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_ads', '0003_alter_adtypesettings_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='predicted_audience_size',
            new_name='audience_size',
        ),
    ]
