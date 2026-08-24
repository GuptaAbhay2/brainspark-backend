from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import User
from game_sessions.models import GameSession

@api_view(['GET'])
@permission_classes([AllowAny])
def global_leaderboard(request):
    """Top 50 users by all-time brain score"""
    users = User.objects.order_by('-brain_score')[:50]
    data = [
        {
            'id': u.id,
            'username': u.username,
            'brain_score': u.brain_score or 0
        }
        for u in users
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def daily_leaderboard(request):
    """Fetch top 50 players based on today's total score"""
    today = timezone.now().date()
    
    daily_scores = (
        GameSession.objects.filter(played_at__date=today)
        .values('user__id', 'user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:50]
    )

    result = [
        {
            'id': item['user__id'],
            'username': item['user__username'],
            'brain_score': item['total_score'] or 0
        }
        for item in daily_scores
    ]
    return Response(result)

@api_view(['GET'])
@permission_classes([AllowAny])
def weekly_leaderboard(request):
    """Top users by score this week"""
    week_ago = timezone.now() - timedelta(days=7)
    
    weekly = (
        GameSession.objects
        .filter(played_at__gte=week_ago)
        .values('user__id', 'user__username')
        .annotate(weekly_score=Sum('score'))
        .order_by('-weekly_score')[:50]
    )
    
    data = [
        {
            'id': w['user__id'],
            'username': w['user__username'],
            'brain_score': w['weekly_score'] or 0,
        }
        for w in weekly
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
            'user_id': user.id,
            'rank': rank,
            'brain_score': user.brain_score,
            'username': user.username,
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)