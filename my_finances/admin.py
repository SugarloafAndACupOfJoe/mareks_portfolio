from django.contrib import admin
from my_finances.models import Income, Outcome, Balance


# Register your models here.
admin.site.register(Income)
admin.site.register(Outcome)
admin.site.register(Balance)
