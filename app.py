"""
DAA Mini Project: Task Focus Planner - "What should I focus on first?"
Algorithm : Greedy Method (always pick the most valuable-per-day task first)
            + recursive Merge Sort (Divide and Conquer) to rank the tasks
Backend   : Python (standard library only - nothing to install)
Frontend  : index.html (HTML + CSS + JavaScript)

How to run:
    python app.py
Then open  http://localhost:8000  (it opens automatically).

How it works:
    1. The user says how many tasks there are (n).
    2. For each task the user enters: name, days left, marks weightage.
    3. Priority score = marks / days          (days = 0 is treated as 1)
          -> more marks and less time left = higher score
    4. Merge Sort arranges the tasks from highest to lowest score.
       (if two scores are equal, the task with more marks comes first)
    5. The first task in the sorted list is the one to focus on first.

Time complexity : O(n log n)  (Merge Sort)       Space complexity : O(n)
"""

import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000
HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------
#  1. PRIORITY SCORE (the greedy criterion)
# ----------------------------------------------------------------------
def calculate_score(days, marks):
    days = max(days, 1)                 # due today (0 days) -> treat as 1
    return marks / days


# ----------------------------------------------------------------------
#  2. MERGE SORT (recursive, highest score first)
# ----------------------------------------------------------------------
def comes_first(a, b):
    """True if task a should be placed before task b."""
    if a["score"] != b["score"]:
        return a["score"] > b["score"]
    return a["marks"] >= b["marks"]      # tie -> more marks first (stable)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if comes_first(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(tasks):
    if len(tasks) <= 1:                  # base case
        return tasks
    mid = len(tasks) // 2
    left = merge_sort(tasks[:mid])       # divide
    right = merge_sort(tasks[mid:])
    return merge(left, right)            # combine


# ----------------------------------------------------------------------
#  3. BUILD THE PRIORITY LIST
# ----------------------------------------------------------------------
def level_for(score, top_score):
    """High / Medium / Low relative to the best task."""
    ratio = score / top_score if top_score else 0
    if ratio >= 0.66:
        return "High"
    if ratio >= 0.33:
        return "Medium"
    return "Low"


def make_priority_list(tasks):
    for t in tasks:
        t["score"] = calculate_score(t["days"], t["marks"])
    ranked = merge_sort(tasks)
    top = ranked[0]["score"]

    result = []
    for i, t in enumerate(ranked, 1):
        result.append({
            "rank": i, "name": t["name"], "days": t["days"], "marks": t["marks"],
            "score": round(t["score"], 2), "level": level_for(t["score"], top),
        })

    first = result[0]
    when = "today" if first["days"] == 0 else f"in {first['days']} day(s)"
    reason = (f"'{first['name']}' carries {first['marks']} marks and is due {when}, "
              f"so it gives the most marks per day left (score {first['score']}).")
    return {"ranked": result, "focus_first": first["name"], "reason": reason}


def validate(data):
    tasks = []
    for t in data.get("tasks", []):
        name = str(t.get("name", "")).strip()
        if not name:
            raise ValueError("Every task needs a name.")
        days, marks = float(t.get("days", -1)), float(t.get("marks", 0))
        if days != int(days) or days < 0:
            raise ValueError(f"Days left for '{name}' must be a whole number (0 or more).")
        if marks != int(marks) or marks < 1:
            raise ValueError(f"Marks for '{name}' must be a whole number (1 or more).")
        tasks.append({"name": name, "days": int(days), "marks": int(marks)})
    if not tasks:
        raise ValueError("Enter at least one task.")
    return tasks


# ----------------------------------------------------------------------
#  TINY WEB SERVER (serves index.html and one API route)
# ----------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        else:
            self._send(404, b"Not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/priority":
            self._send(404, b"Not found", "text/plain")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            tasks = validate(json.loads(self.rfile.read(length)))
            self._send(200, json.dumps(make_priority_list(tasks)).encode(),
                       "application/json")
        except (ValueError, TypeError, json.JSONDecodeError) as err:
            self._send(400, json.dumps({"error": str(err)}).encode(), "application/json")

    def log_message(self, *args):        # keep the terminal clean
        pass


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"Task Focus Planner running at {url}  (press Ctrl+C to stop)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")