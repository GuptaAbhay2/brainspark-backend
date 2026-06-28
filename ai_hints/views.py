import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from puzzles.models import Puzzle

@api_view(['POST'])
@permission_classes([AllowAny])
def get_hint(request):
    """
    Generate AI hint using Gemini API (free).
    Falls back to pre-written hint if API key not set.
    """
    puzzle_id   = request.data.get('puzzle_id')
    user_answer = request.data.get('user_answer', '')

    try:
        puzzle = Puzzle.objects.get(id=puzzle_id)
    except Puzzle.DoesNotExist:
        return Response({'error': 'Puzzle not found'}, status=404)

    # Try Gemini API first
    api_key = os.getenv('GEMINI_API_KEY', '')
    if api_key:
        hint = _gemini_hint(puzzle, user_answer, api_key)
    else:
        # Fallback to pre-written hint
        hint = puzzle.hint_text or "Try breaking the problem into smaller steps!"

    return Response({'hint': hint})


def _gemini_hint(puzzle, user_answer, api_key):
    """Call Gemini API to generate a smart hint"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""You are a friendly puzzle coach for a brain game app.
Puzzle type: {puzzle.type}
Puzzle data: {puzzle.data}
User's current answer: {user_answer}

Give a SHORT hint (2-3 lines max) that guides the user toward the solution 
WITHOUT giving the answer directly. Be encouraging and simple.
Respond in simple English."""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return puzzle.hint_text or "Look for patterns — something repeats!"
