"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer


class GamerView(ViewSet):
    """Honey Rae API customers view"""

    def list(self, request):
        """Handle GET requests to get all customers

        Returns:
            Response -- JSON serialized list of customers
        """

        gamers = Gamer.objects.all()
        serialized = GamerSerializer(gamers, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer record
        """

        gamer = Gamer.objects.get(pk=pk)
        serialized = GamerSerializer(gamer, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""
    class Meta:
        model = Gamer
        fields = ('id', 'full_name', 'bio')