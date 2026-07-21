# Generated manually for Phase 3 export artifacts.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cleaning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cleaningjob",
            name="cleaned_csv_file",
            field=models.FileField(blank=True, null=True, upload_to="cleaned/"),
        ),
        migrations.AddField(
            model_name="cleaningjob",
            name="cleaned_xlsx_file",
            field=models.FileField(blank=True, null=True, upload_to="cleaned/"),
        ),
        migrations.AddField(
            model_name="cleaningjob",
            name="selected_actions",
            field=models.JSONField(default=dict),
        ),
    ]
