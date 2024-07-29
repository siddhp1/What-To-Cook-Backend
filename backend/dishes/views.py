from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Dish
from .serializers import DishSerializer, DishLimitedSerializer

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all().order_by('-date_last_made')
    serializer_class = DishSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'cuisine']
    ordering_fields = ['date_last_made', 'cuisine', 'name']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def update(self, request, *args, **kwargs):
        print("Request User:", request.user)
        dish = self.get_object()
        if dish.user != request.user:
            return Response({'detail': 'You do not have permission to update this dish.'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)
    
class DishRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Query for quick dishes with a time_to_cook score of 1 or 2
        quick_dishes = Dish.objects.filter(Q(time_to_make=1) | Q(time_to_make=2), user=request.user).order_by('?')[:20]
        
        # Query for favorite dishes with a rating of 8, 9, or 10
        favorite_dishes = Dish.objects.filter(Q(rating=8) | Q(rating=9) | Q(rating=10), user=request.user).order_by('?')[:20]
        
        # Query for the 20 dishes with the oldest date last made
        oldest_dishes = Dish.objects.filter(user=request.user).order_by('date_last_made')[:20]
        
        # Serialize the data
        quick_dishes_serializer = DishLimitedSerializer(quick_dishes, many=True, context={'request': request})
        favorite_dishes_serializer = DishLimitedSerializer(favorite_dishes, many=True, context={'request': request})
        oldest_dishes_serializer = DishLimitedSerializer(oldest_dishes, many=True, context={'request': request})
        
        # Combine the serialized data into one JSON response
        response_data = {
            'quick_dishes': quick_dishes_serializer.data,
            'favorite_dishes': favorite_dishes_serializer.data,
            'oldest_dishes': oldest_dishes_serializer.data
        }
        
        # Return the combined serialized data
        return Response(response_data)