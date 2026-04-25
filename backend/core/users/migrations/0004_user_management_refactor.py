# Generated manually (Django 6.x compatible).

from django.db import migrations, models
from django.db.models.functions import Lower


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_options_alter_user_role_alter_user_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("admin", "Admin"), ("user", "User")],
                db_index=True,
                default="user",
                max_length=20,
            ),
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"permissions": [("is_admin", "General Administrative Access")]},
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                Lower("email"),
                name="users_email_ci_unique",
            ),
        ),
    ]

