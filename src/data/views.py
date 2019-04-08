from .models import DataBasin
from rest_framework import generics, permissions, pagination
from .permissions import IsOwnerOrReadOnly
from .serializers import DataBasinSerializer,DataPluvioSerializer


class DataBasinDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset            = DataBasin.objects.all()
    serializer_class    = DataBasinSerializer
    lookup_field        = 'pk'
    permission_classes  = [IsOwnerOrReadOnly]

class DataBasinListAPIView(generics.ListCreateAPIView):
    queryset            = DataBasin.objects.all()
    serializer_class    = DataBasinSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
