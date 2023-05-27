from django.contrib.auth.models import User

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Recipe, Rating, Comment, Ingredients
from .serializers import RecipeSerializer, RatingSerializer, UserSerializer, CommentSerializer, IngredientsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def rate_recipe(self, request, pk=None):
        if 'stars' in request.data:

            recipe = Recipe.objects.get(id=pk)
            stars = request.data['stars']
            user = User.objects.get(id=1)
            # user = request.user
            print(user)

            try:
                rating = Rating.objects.get(user=user.id, recipe=recipe.id)
                rating.stars = stars
                rating.save()

                serializer = RatingSerializer(rating, many=False)

                response = {
                    'message': 'Rating Updated',
                    'result': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)

            except:
                rating = Rating.objects.create(
                    user=user, recipe=recipe, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {
                    'message': 'Rating Created',
                    'result': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'Yo need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], authentication_classes=(TokenAuthentication, ))
    def comment_recipe(self, request, pk=None):

        # Get the recipe
        recipe = Recipe.objects.get(id=pk)
        user = User.objects.get(id=1)
        comment_body = request.data['body']

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'message': 'You must be authenticated to comment.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create the comment
        new_comment = Comment.objects.create(
            user_id=user,
            body=comment_body,
            parent_recipe=recipe,
        )
        # new_comment.save()
        recipe.comments.add(new_comment)

        # Serialize the comments
        serializer = CommentSerializer(new_comment, many=False)

        # Return the response
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'], authentication_classes=(TokenAuthentication, ))
    def add_ingredients(self, request, pk=None):
        ingredients_title = request.data['title']
        ingredients_amount = request.data['amount']
        ingredients_image = request.data['image']

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'message': 'You must be authenticated to Ingredients.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create the Ingredients
        new_Ingredients = Ingredients.objects.create(
            # user_id=user,
            title=ingredients_title,
            amount=ingredients_amount,
            image=ingredients_image
        )
        # new_Ingredients.save()
        # recipe.Ingredientss.add(new_Ingredients)

        # Serialize the Ingredientss
        serializer = IngredientsSerializer(new_Ingredients, many=False)

        # Return the response
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        title = request.data['title']
        body = request.data['body']
        user_id = User.objects.get(id=1)
        summary = request.data['summary']
        slug = request.data['slug']
        tricks = request.data['tricks']
        for_how_many_people = request.data['for_how_many_people']
        time_to_cook = request.data['time_to_cook']
        time_to_get_it_ready = request.data['ttime_to_get_it_readyitle']

        response = {'message': 'Yo cant create Recipe like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        response = {'message': 'Yo cant Update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Yo cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
