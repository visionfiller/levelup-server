from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer
from rest_framework.decorators import action
from django.db.models import Count
from django.db.models import Q
from django.core.exceptions import ValidationError


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.annotate(attendee_count=Count('attendees')).get(pk=pk)
            
            
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(
            attendees_count=Count('attendees'),
            joined=Count(
                'attendees',
                filter=Q(attendees=gamer)
            )
)
        
        if "game" in request.query_params:
            if request.query_params['game'] == request.query_params.get('game'):
                    events = events.filter(game= request.query_params.get('game'))
        # Set the `joined` property on every event
        

                    
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    def create(self, request):
            """Handle POST operations

            Returns
                Response -- JSON serialized game instance
            """
            game = Game.objects.get(pk=request.data["game"])
            gamer = Gamer.objects.get(user=request.auth.user)
            serializer = CreateEventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(gamer=gamer)
            serializer.save(game=game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.location = request.data["location"]
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        gamer = Gamer.objects.get(pk=request.data["organizer"])
        event.game = game
        event.organizer = gamer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
        
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'game','location', 'description','attendees', 'date', 'time')
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    attendee_count = serializers.IntegerField(default=None)
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer', 'location', 'description','attendees', 'date', 'time', 'joined', 'attendee_count')
        