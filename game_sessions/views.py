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

    # 1. Fetch User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            'error': f'User with ID {user_id} does not exist in Database.'
        }, status=status.HTTP_404_NOT_FOUND)

    # 2. Fetch Puzzle
    puzzle = None
    if puzzle_id:
        puzzle = Puzzle.objects.filter(id=puzzle_id).first()

    # 3. Create Game Session
    session = GameSession.objects.create(
        user=user,
        puzzle=puzzle,
        score=score or 0,
        time_taken=time_taken or 0,
        hints_used=hints_used or 0,
        completed=completed
    )

    # 4. Safe Score Handling (Prevents NULL + Number crash)
    try:
        added_score = int(score) if score is not None else 0
    except (ValueError, TypeError):
        added_score = 0

    current_brain_score = user.brain_score if user.brain_score is not None else 0
    current_total_games = user.total_games if user.total_games is not None else 0

    user.brain_score = current_brain_score + added_score
    user.total_games = current_total_games + 1

    # 5. Safe Streak Logic
    curr_streak = user.current_streak if user.current_streak is not None else 0
    long_streak = user.longest_streak if user.longest_streak is not None else 0

    today = timezone.now().date()
    if user.last_played:
        diff = (today - user.last_played).days
        if diff == 1:
            curr_streak += 1
        elif diff > 1:
            curr_streak = 1
    else:
        curr_streak = 1

    if curr_streak > long_streak:
        long_streak = curr_streak

    user.current_streak = curr_streak
    user.longest_streak = long_streak
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