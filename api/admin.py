from django.contrib import admin
from .models import Recipe, RecipeImage, Ingredients, Step, StepImage, Comment


admin.site.register(Recipe)
admin.site.register(RecipeImage)
admin.site.register(Ingredients)
admin.site.register(Step)
admin.site.register(StepImage)
admin.site.register(Comment)
