from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Ingredients(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="ingredients", null=True)
    amount = models.CharField(max_length=25)


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    tricks = models.CharField(max_length=255)
    ingredients = models.ManyToManyField('Ingredients')
    steps = models.ManyToManyField('Step')
    images = models.ManyToManyField('RecipeImage')
    for_how_many_people = models.IntegerField()
    comments = models.ManyToManyField('Comment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_to_cook = models.CharField(max_length=255)
    time_to_get_it_ready = models.CharField(max_length=255)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(recipe=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(recipe=self)
        for rating in ratings:
            sum += rating.stars

        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0


class RecipeImage(models.Model):
    image = models.ImageField(upload_to="recipeImages")


class Step(models.Model):
    number = models.IntegerField()
    instruction = models.TextField()
    images = models.ManyToManyField('StepImage')


class StepImage(models.Model):
    images = models.ImageField(upload_to="StepImages")


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    parent_recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    replies = models.ManyToManyField('Comment', related_name='parent_comment')


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'recipe'),)
        index_together = (('user', 'recipe'),)
