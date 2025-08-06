from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import StockFilter, StockMovementFilter
from .models import Stock, StockMovement
from .serializers import StockMovementSerializer, StockSerializer


class StockListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter

    def get_queryset(self):
        queryset = Stock.objects.all().select_related("product", "company")
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock = serializer.save()
        return Response(StockSerializer(stock).data, status=status.HTTP_201_CREATED)


class StockRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Stock.objects.all().select_related("product", "company")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StockMovementListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockMovementFilter

    def get_queryset(self):
        queryset = StockMovement.objects.all().select_related("stock")
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock_movement = serializer.save()
        return Response(StockMovementSerializer(stock_movement).data, status=status.HTTP_201_CREATED)


class StockMovementRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockMovementSerializer
    lookup_field = "id"

    def get_queryset(self):
        return StockMovement.objects.all().select_related("stock")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
