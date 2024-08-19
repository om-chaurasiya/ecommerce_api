
from rest_framework import generics, permissions, status
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserProfileView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # If the user is a superuser, return all profiles with pagination
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        # Regular users only get their own profile
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        # If the user is a superuser, allow them to retrieve any user profile by specifying the user ID
        if self.request.user.is_superuser:
            # Retrieve a specific user by ID (if needed)
            return get_object_or_404(CustomUser, pk=self.request.user.id)

        # Regular users can only access their own profile
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user or request.user.is_superuser:
            user.delete()
            return Response({"detail": "User profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to delete this profile."},
                        status=status.HTTP_403_FORBIDDEN)