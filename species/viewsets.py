from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Specie
from .serializers import SpecieSerializer


class SpeciesViewSet(ReadOnlyModelViewSet):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer
