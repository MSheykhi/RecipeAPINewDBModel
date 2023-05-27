from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Recipe, Rating, Ingredients, RecipeImage, Step, StepImage, Comment


class IngredientsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    amount = serializers.CharField(max_length=25)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Ingredients
        fields = ('title', 'amount', 'image')


class StepImageSerializer(serializers.ModelSerializer):
    images = serializers.ImageField(read_only=True)

    class Meta:
        model = StepImage
        fields = ('images', )


class RecipeStepSerializer(serializers.ModelSerializer):
    images = StepImageSerializer(many=True)

    class Meta:
        model = Step
        fields = '__all__'


class RecipeImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = RecipeImage
        fields = ('image', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    body = serializers.CharField(required=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'parent_recipe',
                  'replies')
        # fields = ('id', 'user', 'body', 'parent_recipe',
        #           'replies', 'created_at', 'updated_at')


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = IngredientsSerializer(many=True)
    images = RecipeImageSerializer(many=True)
    steps = RecipeStepSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('slug', 'title', 'images', 'summary', 'body', 'steps', 'ingredients', 'tricks',
                  'for_how_many_people', 'comments', 'created_at', 'updated_at', 'no_of_ratings', 'avg_rating', )
        # fields = '__all__'
