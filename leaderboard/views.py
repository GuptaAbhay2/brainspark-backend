from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import User
from game_sessions.models import GameSession
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
@permission_classes([AllowAny])
def global_leaderboard(request):
    """Top 50 users by brain_score"""
    top_users = User.objects.order_by('-brain_score')[:50]
    data = [
        {
            'rank': i + 1,
            'user_id': u.id,
            'username': u.username,
            'avatar': u.avatar,
            'brain_score': u.brain_score,
            'current_streak': u.current_streak,
        }
        for i, u in enumerate(top_users)
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def weekly_leaderboard(request):
    """Top users by score this week"""
    week_ago = timezone.now() - timedelta(days=7)
    from django.db.models import Sum
    weekly = (
        GameSession.objects
        .filter(played_at__gte=week_ago)
        .values('user__id', 'user__username', 'user__avatar')
        .annotate(weekly_score=Sum('score'))
        .order_by('-weekly_score')[:50]
    )
    data = [
        {
            'rank': i + 1,
            'user_id': w['user__id'],
            'username': w['user__username'],
            'avatar': w['user__avatar'],
            'weekly_score': w['weekly_score'],
        }
        for i, w in enumerate(weekly)
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_rank(request, user_id):
    """Get a specific user's rank"""
    try:
        user = User.objects.get(id=user_id)
        rank = User.objects.filter(brain_score__gt=user.brain_score).count() + 1
        return Response({
            'user_id': user_id,
            'rank': rank,
            'brain_score': user.brain_score,
            'username': user.username,
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
