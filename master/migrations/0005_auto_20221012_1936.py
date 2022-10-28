# Generated by Django 3.2.9 on 2022-10-12 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_master_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='master',
            name='specialities',
            field=models.ManyToManyField(related_name='master', to='master.Speciality'),
        ),
    ]