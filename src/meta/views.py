from .models import Basin
from rest_framework import generics, permissions, pagination
from .permissions import IsOwnerOrReadOnly
from .serializers import BasinSerializer


class BasinDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset            = Basin.objects.all()
    serializer_class    = BasinSerializer
    lookup_field        = 'slug'
    permission_classes  = [IsOwnerOrReadOnly]

class BasinListAPIView(generics.ListCreateAPIView):
    queryset            = Basin.objects.all()
    serializer_class    = BasinSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
