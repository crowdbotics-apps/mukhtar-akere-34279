from django.contrib import admin

from home.models import App, Plan, Subscription

# Register your models here.

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'framework', 'domain_name',)
    inlines = (SubscriptionInline, )
    

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', )
    

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'active')
