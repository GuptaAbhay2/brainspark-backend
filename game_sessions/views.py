import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from django.utils import timezone
from .models import GameSession
from users.models import User
from puzzles.models import Puzzle

class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = '__all__'

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_score(request):
    """Submit game result — updates user brain_score and streak safely"""
    user_id    = request.data.get('user_id')
    puzzle_id  = request.data.get('puzzle_id')
    score      = request.data.get('score', 0)
    time_taken = request.data.get('time_taken', 0)
    hints_used = request.data.get('hints_used', 0)
    completed  = request.data.get('completed', False)

    # 1. Fetch User (Strict Check)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            'error': f'User with ID {user_id} does not exist in Database.'
        }, status=status.HTTP_404_NOT_FOUND)

    # 2. Fetch Puzzle (Graceful Fallback - handles missing or invalid puzzle_id)
    puzzle = None
    if puzzle_id:
        puzzle = Puzzle.objects.filter(id=puzzle_id).first()

    # 3. Create Game Session Record
    session = GameSession.objects.create(
        user=user,
        puzzle=puzzle,
        score=score,
        time_taken=time_taken,
        hints_used=hints_used,
        completed=completed
    )

    # 4. Update User Profile Scores
    user.brain_score += int(score)
    user.total_games += 1

    # 5. Streak Logic Calculation
    today = timezone.now().date()
    if user.last_played:
        diff = (today - user.last_played).days
        if diff == 1:
            user.current_streak += 1
        elif diff > 1:
            user.current_streak = 1
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