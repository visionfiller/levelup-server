from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        if "game" in request.query_params:
            if request.query_params['game'] == request.query_params.get('game'):
                    events = events.filter(game= request.query_params.get('game'))
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    def create(self, request):
            """Handle POST operations

            Returns
                Response -- JSON serialized game instance
            """
            game = Game.objects.get(pk=request.data["game"])
            gamer = Gamer.objects.get(pk=request.data["organizer"])

            event = Event.objects.create(
                location=request.data["location"],
                description=request.data["description"],
                date=request.data["date"],
                time=request.data["time"],
                game=game,
                organizer = gamer
            )
            serializer = EventSerializer(event)
            return Response(serializer.data)
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer', 'location', 'description','attendees', 'date', 'time')