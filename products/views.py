from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from utils.mixins import SerializerByMethodMixin

from .models import Product

from .serializers import ProductSerializer, ProductDetailSerializer

from .permissions import IsSellerOrReadOnly, IsSellerUser


class ProductView(SerializerByMethodMixin, ListCreateAPIView):
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }

    def perform_create(self, serializer):

        serializer.save(seller=self.request.user)

class ProductDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsSellerUser]

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer