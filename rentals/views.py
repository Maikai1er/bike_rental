from rest_framework import generics, permissions, status, response
from django.utils import timezone
from .models import User, Bike, Rental
from .serializers import UserSerializer, BikeSerializer, RentalSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BikeListView(generics.ListAPIView):
    queryset = Bike.objects.filter(status='available')
    serializer_class = BikeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RentalCreateView(generics.CreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        bike = serializer.validated_data['bike']
        bike.status = 'rented'
        bike.save()
        serializer.save(user=user)


class RentalReturnView(generics.UpdateAPIView):
    queryset = Rental.objects.filter(end_time__isnull=True)
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        rental = serializer.instance
        rental.end_time = timezone.now()
        rental.price = self.calculate_cost(rental.start_time, rental.end_time)
        rental.bike.status = 'available'
        rental.bike.save()
        rental.save()

    def calculate_cost(self, start_time, end_time):
        return 0  # Заглушка


class UserRentalHistoryView(generics.ListAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(user=user)
