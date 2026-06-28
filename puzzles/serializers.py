from rest_framework import serializers
from .models import Puzzle

class PuzzleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puzzle
        fields = ['id', 'type', 'difficulty', 'data', 'time_limit', 'max_score']
        # solution is NOT included — security!

class PuzzleWithSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puzzle
        fields = '__all__'
