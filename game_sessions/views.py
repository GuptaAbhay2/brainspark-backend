import datetime
import traceback
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
    try:
        user_id    = request.data.get('user_id')
        puzzle_id  = request.data.get('puzzle_id')
        score      = request.data.get('score', 0)
        time_taken = request.data.get('time_taken', 0)
        hints_used = request.data.get('hints_used', 0)
        completed  = request.data.get('completed', False)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User {user_id} not found'}, status=404)

        puzzle = None
        if puzzle_id:
            puzzle = Puzzle.objects.filter(id=puzzle_id).first()

        session = GameSession.objects.create(
            user=user,
            puzzle=puzzle,
            score=score or 0,
            time_taken=time_taken or 0,
            hints_used=hints_used or 0,
            completed=bool(completed)
        )

        user.brain_score = (user.brain_score or 0) + (int(score) if score else 0)
        user.total_games = (user.total_games or 0) + 1

        curr_streak = user.current_streak or 0
        long_streak = user.longest_streak or 0
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

    except Exception as e:
        print("======== EXACT PYTHON CRASH LOG START ========")
        traceback.print_exc()
        print("======== EXACT PYTHON CRASH LOG END ========")
        return Response({'server_crash_error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_history(request, user_id):
    sessions = GameSession.objects.filter(user_id=user_id)[:20]
    return Response(GameSessionSerializer(sessions, many=True).data)