from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from task_management_project import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


class GoogleOAuthConfig(models.Model):
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    redirect_uri = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google OAuth Config ({self.id})"


class Invitation(models.Model):
    email = models.EmailField()
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invitations")
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.invited_by.is_staff:
            raise ValidationError('This can only be performed by admin users')
        context = {"email": self.email, "token_link": self.token}
        temp = render_to_string("sendInvitationToMail.html", context=context)
        msg = EmailMultiAlternatives("Dont reply" ,temp, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.content_subtype = "html"
        msg.send()
        super(Invitation, self).save(*args, **kwargs)    
