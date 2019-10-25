# Generated by Django 2.2.5 on 2019-09-18 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substituter', '0002_auto_20190918_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='carbohydrates',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='fats',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='fibers',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='proteins',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='salt',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sugars',
            field=models.FloatField(null=True),
        ),
    ]