from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from home import managers

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class App(BaseModel):
    TYPE_CHOICES = (
        ('web', 'Web'),
        ('mobile', 'Mobile')
    )
    FRAMEWORK_CHOICES = (
        ('django', 'Django'),
        ('react_native', 'React Native')
    )
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(choices=TYPE_CHOICES, max_length=255)
    framework = models.CharField(choices=FRAMEWORK_CHOICES, max_length=255)
    domain_name = models.CharField(max_length=50, blank=True, null=True)
    screenshot = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def subscription(self):
        last_subscription = self.user.subscriptions.last()
        if last_subscription:
            return last_subscription.id
        return None
        

class Plan(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19)
    
    def __str__(self):
        return self.name


class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="subscriptions")
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="subscriptions")
    active = models.BooleanField()
    objects = managers.ActivePlanManager()
    all_objects = models.Manager()
    
    def __str__(self):
        return "%s-%s" % (self.user, self.plan)
    
    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
