# Generated by Django 4.2.16 on 2024-11-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoiceApp", "0010_record_purchaserate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orders",
            name="purchaseRate",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="record",
            name="purchaseRate",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
