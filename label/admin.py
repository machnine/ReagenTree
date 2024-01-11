from django.contrib import admin
from label.models import LabelSheet
# Register models in the admin site remove the needs for CRUD views
admin.site.register(LabelSheet)
