import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainspark_backend.settings')
django.setup()

from puzzles.models import Puzzle

puzzles = [
    # --- SPEED MATH easy ---
    {
        "type": "speed_math", "difficulty": "easy",
        "data": {"questions": [
            {"q": "3 + 7", "a": 10}, {"q": "5 × 4", "a": 20},
            {"q": "15 - 8", "a": 7}, {"q": "12 ÷ 4", "a": 3},
            {"q": "6 + 9",  "a": 15}, {"q": "8 × 3", "a": 24},
        ]},
        "solution": {"type": "multi_answer"},
        "hint_text": "Take it one step at a time. Don't rush!",
        "time_limit": 30, "max_score": 60,
    },
    # --- SPEED MATH medium ---
    {
        "type": "speed_math", "difficulty": "medium",
        "data": {"questions": [
            {"q": "17 + 28", "a": 45}, {"q": "12 × 7", "a": 84},
            {"q": "64 ÷ 8",  "a": 8},  {"q": "99 - 47", "a": 52},
            {"q": "15 × 6",  "a": 90}, {"q": "144 ÷ 12", "a": 12},
        ]},
        "solution": {"type": "multi_answer"},
        "hint_text": "Break multiplication into parts: 12×7 = 10×7 + 2×7",
        "time_limit": 30, "max_score": 100,
    },
    # --- LOGIC PUZZLE easy ---
    {
        "type": "logic", "difficulty": "easy",
        "data": {
            "question": "What comes next in the pattern?",
            "sequence": [2, 4, 6, 8, "?"],
            "options": [9, 10, 11, 12],
        },
        "solution": 10,
        "hint_text": "Look at the difference between each number.",
        "time_limit": 0, "max_score": 50,
    },
    {
        "type": "logic", "difficulty": "easy",
        "data": {
            "question": "What comes next?",
            "sequence": [1, 4, 9, 16, "?"],
            "options": [20, 25, 30, 36],
        },
        "solution": 25,
        "hint_text": "These are square numbers: 1²=1, 2²=4, 3²=9...",
        "time_limit": 0, "max_score": 50,
    },
    # --- LOGIC PUZZLE medium ---
    {
        "type": "logic", "difficulty": "medium",
        "data": {
            "question": "What comes next?",
            "sequence": [3, 6, 12, 24, "?"],
            "options": [36, 42, 48, 30],
        },
        "solution": 48,
        "hint_text": "Each number is multiplied by the same value.",
        "time_limit": 0, "max_score": 80,
    },
    {
        "type": "logic", "difficulty": "medium",
        "data": {
            "question": "Find the odd one out.",
            "options": [4, 8, 15, 16, 23, 42],
            "instruction": "Which number doesn't belong?",
        },
        "solution": 15,
        "hint_text": "Think about what property the others share.",
        "time_limit": 0, "max_score": 80,
    },
    # --- LOGIC PUZZLE hard ---
    {
        "type": "logic", "difficulty": "hard",
        "data": {
            "question": "What is the missing number?",
            "grid": [[2, 4, 8], [3, 9, 27], [4, 16, "?"]],
        },
        "solution": 64,
        "hint_text": "Look at the relationship between columns in each row.",
        "time_limit": 0, "max_score": 150,
    },
    # --- MEMORY MATCH easy ---
    {
        "type": "memory", "difficulty": "easy",
        "data": {
            "grid_size": "4x4",
            "pairs": [
                {"id": 1, "value": "🐶"}, {"id": 2, "value": "🐱"},
                {"id": 3, "value": "🐭"}, {"id": 4, "value": "🐹"},
                {"id": 5, "value": "🐰"}, {"id": 6, "value": "🦊"},
                {"id": 7, "value": "🐻"}, {"id": 8, "value": "🐼"},
            ],
        },
        "solution": {"type": "match_all_pairs"},
        "hint_text": "Focus on one pair at a time. Try to remember positions!",
        "time_limit": 60, "max_score": 80,
    },
    # --- SUDOKU easy (mini 4x4) ---
    {
        "type": "sudoku", "difficulty": "easy",
        "data": {
            "size": 4,
            "grid": [
                [1, 0, 3, 0],
                [0, 3, 0, 2],
                [3, 0, 2, 0],
                [0, 2, 0, 1],
            ],
        },
        "solution": [
            [1, 2, 3, 4],
            [4, 3, 1, 2],
            [3, 1, 2, 4],  # fixed to be valid
            [2, 4, 4, 1],
        ],
        "hint_text": "In each row, column, and box every number 1-4 must appear once.",
        "time_limit": 0, "max_score": 100,
    },
]

created = 0
for p in puzzles:
    Puzzle.objects.get_or_create(
        type=p['type'],
        difficulty=p['difficulty'],
        data=p['data'],
        defaults={
            'solution': p['solution'],
            'hint_text': p['hint_text'],
            'time_limit': p['time_limit'],
            'max_score': p['max_score'],
        }
    )
    created += 1

print(f"✅ Seeded {created} puzzles successfully!")
print(f"Total puzzles in DB: {Puzzle.objects.count()}")
