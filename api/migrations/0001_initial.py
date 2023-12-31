# Generated by Django 4.2.3 on 2023-07-26 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Responses",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_Name", models.CharField(max_length=50)),
                ("last_Name", models.CharField(blank=True, max_length=50, null=True)),
                ("mobile_No", models.CharField(max_length=15)),
                ("email_Id", models.EmailField(max_length=254)),
                ("monthly_Saving", models.BigIntegerField(default=0)),
                ("monthly_Income", models.BigIntegerField(default=0)),
            ],
        ),
    ]
