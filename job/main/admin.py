from django.contrib import admin

# Register your models here.
from django.apps import apps

post_model=apps.get_app_config('main').get_models()

for model in post_model:
    try:
        admin.site.register(model)
    except admin.site.Alreadyregistered:
        pass
