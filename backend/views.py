from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskInputSerializer
from .scoring import compute_scores, CycleDetected
from datetime import datetime

STRATEGIES = {
    "smart": {"u": 0.35, "i": 0.35, "e": 0.15, "d": 0.15},
    "fastest": {"u": 0.10, "i": 0.10, "e": 0.70, "d": 0.10},
    "impact": {"u": 0.10, "i": 0.70, "e": 0.10, "d": 0.10},
    "deadline": {"u": 0.70, "i": 0.10, "e": 0.10, "d": 0.10},
}

class AnalyzeView(APIView):
    def post(self, request):
        tasks_data = request.data.get("tasks", [])
        strategy = request.data.get("strategy", "smart")
        weights = STRATEGIES.get(strategy, STRATEGIES["smart"])

        validated = []
        for t in tasks_data:
            ser = TaskInputSerializer(data=t)
            ser.is_valid(raise_exception=True)
            item = ser.validated_data
            # parse date if needed
            if "due_date" in item and isinstance(item["due_date"], str):
                item["due_date"] = datetime.strptime(item["due_date"], "%Y-%m-%d").date()
            validated.append(item)

        try:
            result = compute_scores(validated, weights)
        except CycleDetected as e:
            return Response({"error": str(e)}, status=400)

        return Response({"tasks": result})


class SuggestView(APIView):
    def get(self, request):
        # sample tasks (you can remove)
        return Response({"message": "Upload tasks via analyze endpoint first."})
