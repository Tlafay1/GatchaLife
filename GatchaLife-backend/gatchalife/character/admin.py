from django.contrib import admin

from .models import Character, CharacterVariant, Series, VariantReferenceImage

admin.site.register(Character)
admin.site.register(CharacterVariant)
admin.site.register(Series)
admin.site.register(VariantReferenceImage)
