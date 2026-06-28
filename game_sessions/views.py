from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from django.utils import timezone
from .models import GameSession
from users.models import User
from puzzles.models import Puzzle
import datetime

class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = '__all__'

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_score(request):
    """Submit game result — updates user brain_score and streak"""
    user_id    = request.data.get('user_id')
    puzzle_id  = request.data.get('puzzle_id')
    score      = request.data.get('score', 0)
    time_taken = request.data.get('time_taken', 0)
    hints_used = request.data.get('hints_used', 0)
    completed  = request.data.get('completed', False)

    try:
        user   = User.objects.get(id=user_id)
        puzzle = Puzzle.objects.get(id=puzzle_id)
    except (User.DoesNotExist, Puzzle.DoesNotExist):
        return Response({'error': 'User or Puzzle not found'}, status=404)

    # Create session
    session = GameSession.objects.create(
        user=user, puzzle=puzzle,
        score=score, time_taken=time_taken,
        hints_used=hints_used, completed=completed
    )

    # Update user brain_score + total_games
    user.brain_score += score
    user.total_games += 1

    # Update streak
    today = timezone.now().date()
    if user.last_played:
        diff = (today - user.last_played).days
        if diff == 1:
            user.current_streak += 1
        elif diff > 1:
            user.current_streak = 1
        # diff == 0 means already played today, no change
    else:
        user.current_streak = 1

    if user.current_streak > user.longest_streak:
        user.longest_streak = user.current_streak

    user.last_played = today
    user.save()

    return Response({
        'session_id': session.id,
        'brain_score': user.brain_score,
        'current_streak': user.current_streak,
        'longest_streak': user.longest_streak,
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_history(request, user_id):
    """Get last 20 sessions for a user"""
    sessions = GameSession.objects.filter(user_id=user_id)[:20]
    return Response(GameSessionSerializer(sessions, many=True).data)
