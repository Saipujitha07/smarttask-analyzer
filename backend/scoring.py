from datetime import date

class CycleDetected(Exception):
    pass

def detect_cycle(task_map):
    visited = set()
    stack = set()

    def dfs(task_id):
        if task_id in stack:
            raise CycleDetected(f"Cycle detected at task {task_id}")
        if task_id in visited:
            return
        visited.add(task_id)
        stack.add(task_id)
        for dep in task_map[task_id]["dependencies"]:
            if dep in task_map:
                dfs(dep)
        stack.remove(task_id)

    for t in task_map:
        dfs(t)


def compute_scores(tasks, weights):
    task_map = {t["id"]: t for t in tasks}

    detect_cycle(task_map)

    today = date.today()

    # Count how many tasks each task is blocking
    block_count = {t["id"]: 0 for t in tasks}
    for t in tasks:
        for d in t.get("dependencies", []):
            if d in block_count:
                block_count[d] += 1

    max_block = max(block_count.values()) if block_count else 1

    results = []

    for task in tasks:
        # urgency
        due = task.get("due_date")
        if due:
            days_left = (due - today).days
            if days_left < 0:
                urgency = 1 + min(0.5, abs(days_left) / 30)
            else:
                urgency = max(0, (30 - min(days_left, 30)) / 30)
        else:
            urgency = 0.1

        # importance
        importance = (task.get("importance", 5) - 1) / 9

        # effort
        hours = task.get("estimated_hours", 1)
        effort = 1 / (1 + hours)

        # dependency score
        dep_score = block_count[task["id"]] / max_block if max_block else 0

        score = (
            weights["u"] * urgency +
            weights["i"] * importance +
            weights["e"] * effort +
            weights["d"] * dep_score
        )

        explanation = []
        if urgency > 0.8: explanation.append("Urgent")
        if importance > 0.6: explanation.append("High importance")
        if effort > 0.5: explanation.append("Quick win")
        if dep_score > 0.5: explanation.append("Blocks other tasks")

        results.append({
            **task,
            "score": round(score, 4),
            "explanation": ", ".join(explanation) or "Balanced priority"
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
