# Task Priority System

A simple web-based tool that tells you which task to focus on first. You enter the number of tasks, then each task's name, days left and marks weightage. The system ranks them and shows a priority list.

Built as a mini project for **Design and Analysis of Algorithms (DAA)**.

## How it works

1. The user enters the number of tasks.
2. For each task, the user enters the name, days left and marks weightage.
3. Python calculates a priority score for every task:

   ```
   score = marks / days left        (0 days is treated as 1)
   ```

4. The tasks are sorted from highest to lowest score using a recursive **Merge Sort** (divide and conquer). If two scores are equal, the task with more marks comes first.
5. The first task in the sorted list is the one to focus on first (the greedy choice). Each task is labelled High, Medium or Low priority.

## Algorithms used

- **Greedy method**: always pick the task that gives the most marks per day left.
- **Merge Sort**: recursive divide-and-conquer sorting.

## Complexity

| Part | Time | Space |
|------|------|-------|
| Score calculation | O(n) | O(n) |
| Merge Sort | O(n log n) | O(n) |
| Whole program | O(n log n) | O(n) |

## Technologies

- Python 3 (standard library only, no installation needed)
- HTML, CSS and JavaScript for the interface

## Project structure

```
task-priority-system/
├── app.py        # Python: algorithm and local web server
├── index.html    # Web page (HTML, CSS, JavaScript)
└── README.md
```

## How to run

1. Make sure Python 3 is installed.
2. Download or clone this repository.
3. Open a terminal in the project folder and run:

   ```
   python app.py
   ```

4. Open `http://localhost:8000` in your browser if it does not open automatically.
5. Press `Ctrl + C` in the terminal to stop the server.

## Example

| Task | Days left | Marks |
|------|-----------|-------|
| Maths Quiz | 1 | 10 |
| Python Lab | 3 | 20 |
| DAA Project | 5 | 30 |

Scores: 10.00, 6.67 and 6.00, so the priority order is Maths Quiz, then Python Lab, then DAA Project.

## Limitations

- The score formula and the High/Medium/Low cut-offs are design choices and may not suit every situation.
- Tasks are not saved between runs.

## Author

Nithin Manoj
MCA (AI/ML), Chandigarh University


