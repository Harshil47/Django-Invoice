# Generated by Django 4.2.16 on 2024-11-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoiceApp", "0012_payment_df2_payment_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="oid",
            field=models.TextField(blank=True, null=True),
        ),
    ]
