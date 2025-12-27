#🎯 Number Guessing Game
A Python-based GUI number guessing game built with Tkinter. Features multiple difficulty levels, scoring, hints, statistics, and a persistent leaderboard.

#Features
🎮 Interactive GUI – Clean, modern interface with visual feedback

📊 Multiple Difficulties – Easy, Medium, and Hard modes

🏆 Leaderboard System – Saves top 10 scores locally in JSON format

🔍 Smart Hints – Dynamic hints that adapt as you play

📈 Game Statistics – Track wins, streaks, best scores, and win rate

⌨️ Keyboard Shortcuts – Quick access via Ctrl+N (new game) and F1 (hint)

#🎨 Visual Feedback – Color-coded responses and icons for guesses

Requirements
Python 3.x

tkinter (usually included with Python)

#How to Run
bash
python Number_Guessing.py
Game Rules
Choose a difficulty level (Easy: 1–50, Medium: 1–100, Hard: 1–200)

Guess the secret number within the allowed attempts

Each wrong guess reduces your score

Use hints sparingly—they also reduce your score

Win by guessing correctly before running out of attempts

Files
Number_Guessing.py – Main game file

leaderboard.json – Automatically created to store high scores
