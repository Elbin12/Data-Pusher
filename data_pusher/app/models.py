from django.db import models
import secrets

# Create your models here.

class Account(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255, unique=True, editable=False, default=secrets.token_hex)
    website = models.URLField(blank=True, null=True)

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])
    headers = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['account', 'url', 'http_method'], 
                name='unique_account_url_method'
            )
        ]
