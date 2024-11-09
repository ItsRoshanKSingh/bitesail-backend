from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.core.models import Recipe, Tag, Ingredient
from apps.recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer,
    IngredientSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    View for managing recipe APIs.

    This viewset provides the standard CRUD actions for the Recipe model.
    It uses token-based authentication and requires the user to be authenticated.
    The queryset is filtered to only include recipes created by the authenticated user.
    """

    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override to filter recipes by the authenticated user and order by ID.

        Returns:
            Queryset of Recipe objects filtered by the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class depending on the action.

        For the 'list' action, it uses the RecipeSerializer. For other actions,
        it uses the RecipeDetailSerializer.

        Returns:
            Serializer class based on the current action.
        """
        return RecipeSerializer if self.action == "list" else self.serializer_class

    def perform_create(self, serializer):
        """
        Save the recipe with the authenticated user as the owner.

        This method ensures that the user field is set to the currently authenticated user
        when creating a new recipe.

        Args:
            serializer: The serializer instance for the recipe being created.
        """
        serializer.save(user=self.request.user)


class TagViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    View for managing tag APIs.

    This viewset provides a list view for the Tag model, allowing users to retrieve
    the tags they have created. It uses token-based authentication and requires the user
    to be authenticated. The queryset is filtered to only include tags created by the authenticated user.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override to filter tags by the authenticated user and order by name.

        Returns:
            Queryset of Tag objects filtered by the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-name")
