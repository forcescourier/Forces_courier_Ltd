from django.db import models

# notification model

class Notification(models.Model):
    notification_id=models.AutoField(primary_key=True)
    notification_title=models.CharField(max_length=200)
    notification_content=models.TextField()
    notification_created_at=models.DateTimeField(auto_now_add=True)
    notification_updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.notification_title