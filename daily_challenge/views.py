from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import DailyChallenge
from puzzles.models import Puzzle
from puzzles.serializers import PuzzleSerializer
import random

@api_view(['GET'])
@permission_classes([AllowAny])
def get_today(request):
    """Get today's daily challenge — same puzzle for all users"""
    today = timezone.now().date()
    challenge, created = DailyChallenge.objects.get_or_create(
        date=today,
        defaults={
            'puzzle': _pick_random_puzzle()
        }
    )
    return Response({
        'date': str(today),
        'puzzle': PuzzleSerializer(challenge.puzzle).data,
        'is_new': created,
    })

def _pick_random_puzzle():
    """Pick a random medium puzzle for daily challenge"""
    puzzles = Puzzle.objects.filter(difficulty='medium')
    if puzzles.exists():
        return random.choice(list(puzzles))
    return Puzzle.objects.first()
