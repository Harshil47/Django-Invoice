# Generated by Django 4.2.16 on 2024-11-01 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoiceApp", "0007_alter_orders_lno"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "sales_challan_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("product", models.CharField(blank=True, max_length=255, null=True)),
                ("hsn", models.CharField(blank=True, max_length=20, null=True)),
                ("amount", models.FloatField(blank=True, null=True)),
                ("date", models.DateField(blank=True, null=True)),
            ],
        ),
    ]