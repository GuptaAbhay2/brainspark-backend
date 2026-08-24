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
        score      = int(request.data.get('score', 0))
        time_taken = int(request.data.get('time_taken', 0))
        hints_used = request.data.get('hints_used', 0)
        completed  = request.data.get('completed', False)

        # Handle string booleans from JSON safely
        if isinstance(completed, str):
            completed = completed.lower() in ['true', '1']
        else:
            completed = bool(completed)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User {user_id} not found'}, status=404)

        # User ka latest session fetch karo
        last_session = GameSession.objects.filter(user=user).order_by('-id').first()

        is_refresh = False

        # 🛑 REFRESH DETECTORS:
        # 1. Score 0 ya negative ho
        if score <= 0:
            is_refresh = True

        # 2. Score user ke Total Brain Score ke barabar sent hua ho
        if user.brain_score and user.brain_score > 0 and score == user.brain_score:
            is_refresh = True

        # 3. Game completion markers (puzzle_id and completed flag) missing hon
        if not puzzle_id and not completed:
            is_refresh = True

        # 4. Same score baar-baar refresh pe re-submit ho raha ho
        if last_session and last_session.score == score:
            if not puzzle_id or not completed:
                is_refresh = True

        # Agar Refresh request hai toh DB score increment SKIP karo
        if is_refresh:
            return Response({
                'session_id': last_session.id if last_session else None,
                'brain_score': user.brain_score or 0,
                'current_streak': user.current_streak or 0,
                'longest_streak': user.longest_streak or 0,
            }, status=status.HTTP_200_OK)

        # ✅ REAL GAMEPLAY SESSION:
        puzzle = None
        if puzzle_id:
            puzzle = Puzzle.objects.filter(id=puzzle_id).first()

        session = GameSession.objects.create(
            user=user,
            puzzle=puzzle,
            score=score,
            time_taken=time_taken,
            hints_used=hints_used or 0,
            completed=completed
        )

        user.brain_score = (user.brain_score or 0) + score
        user.total_games = (user.total_games or 0) + 1

        today = timezone.now().date()
        curr_streak = user.current_streak or 0
        long_streak = user.longest_streak or 0

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