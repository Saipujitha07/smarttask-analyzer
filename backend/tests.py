from django.test import SimpleTestCase
from datetime import date, timedelta
from .scoring import compute_scores, CycleDetected

class ScoringTests(SimpleTestCase):

    def test_urgency_scoring(self):
        """Task due today should have higher urgency than task due in 10 days."""
        today = date.today()
        future = date.today() + timedelta(days=10)

        tasks = [
            {"id": "1", "title": "A", "due_date": today, "estimated_hours": 2, "importance": 5, "dependencies": []},
            {"id": "2", "title": "B", "due_date": future, "estimated_hours": 2, "importance": 5, "dependencies": []},
        ]

        weights = {"u": 1, "i": 0, "e": 0, "d": 0}

        result = compute_scores(tasks, weights)

        self.assertGreater(result[0]["score"], result[1]["score"])

    def test_effort_scoring(self):
        """Task with lower effort should have higher score."""
        tasks = [
            {"id": "1", "title": "Easy", "due_date": None, "estimated_hours": 1, "importance": 5, "dependencies": []},
            {"id": "2", "title": "Hard", "due_date": None, "estimated_hours": 10, "importance": 5, "dependencies": []},
        ]

        weights = {"u": 0, "i": 0, "e": 1, "d": 0}

        result = compute_scores(tasks, weights)

        self.assertGreater(result[0]["score"], result[1]["score"])

    def test_dependency_blocking(self):
        """Task that blocks more tasks should rank higher."""
        tasks = [
            {"id": "1", "title": "Root", "due_date": None, "estimated_hours": 2, "importance": 5, "dependencies": []},
            {"id": "2", "title": "Child1", "due_date": None, "estimated_hours": 2, "importance": 5, "dependencies": ["1"]},
            {"id": "3", "title": "Child2", "due_date": None, "estimated_hours": 2, "importance": 5, "dependencies": ["1"]},
        ]

        weights = {"u": 0, "i": 0, "e": 0, "d": 1}

        result = compute_scores(tasks, weights)

        # Root blocks 2 tasks, so should be first
        self.assertEqual(result[0]["id"], "1")

    def test_cycle_detection(self):
        """Circular dependencies should raise CycleDetected."""
        tasks = [
            {"id": "1", "title": "A", "due_date": None, "estimated_hours": 1, "importance": 5, "dependencies": ["2"]},
            {"id": "2", "title": "B", "due_date": None, "estimated_hours": 1, "importance": 5, "dependencies": ["1"]},
        ]

        weights = {"u": 1, "i": 1, "e": 1, "d": 1}

        with self.assertRaises(CycleDetected):
            compute_scores(tasks, weights)
