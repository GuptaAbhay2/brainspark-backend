import random
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Puzzle
from .serializers import PuzzleSerializer, PuzzleWithSolutionSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_puzzles(request):
    """Get puzzles by type and difficulty"""
    puzzle_type = request.query_params.get('type', 'sudoku')
    difficulty  = request.query_params.get('difficulty', 'easy')
    puzzles = Puzzle.objects.filter(type=puzzle_type, difficulty=difficulty)
    # Return random puzzle from filtered list
    if puzzles.exists():
        puzzle = random.choice(puzzles)
        return Response(PuzzleSerializer(puzzle).data)
    return Response({'error': 'No puzzles found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_puzzles(request):
    """Get all puzzles list — for offline caching in Flutter"""
    puzzle_type = request.query_params.get('type')
    qs = Puzzle.objects.all()
    if puzzle_type:
        qs = qs.filter(type=puzzle_type)
    return Response(PuzzleSerializer(qs, many=True).data)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_solution(request):
    """Check if submitted answer is correct"""
    puzzle_id = request.data.get('puzzle_id')
    answer    = request.data.get('answer')
    try:
        puzzle = Puzzle.objects.get(id=puzzle_id)
        is_correct = puzzle.solution == answer
        return Response({
            'correct': is_correct,
            'solution': puzzle.solution if not is_correct else None,
            'hint': puzzle.hint_text if not is_correct else None,
        })
    except Puzzle.DoesNotExist:
        return Response({'error': 'Puzzle not found'}, status=status.HTTP_404_NOT_FOUND)
