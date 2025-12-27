import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os
from datetime import datetime

class EnhancedGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("500x650")
        self.root.configure(bg="#2C3E50")
        
        # Game settings
        self.difficulty = "medium"
        self.difficulty_settings = {
            "easy": {"max": 50, "attempts": 10, "multiplier": 1.0},
            "medium": {"max": 100, "attempts": 7, "multiplier": 1.5},
            "hard": {"max": 200, "attempts": 5, "multiplier": 2.0}
        }
        
        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.score = 0
        self.game_active = False
        self.max_number = 100
        self.max_attempts = 7
        self.hints_used = 0
        
        # Statistics
        self.stats = {"games_played": 0, "games_won": 0, "best_score": 0, "streak": 0}
        self.leaderboard = self.load_leaderboard()
        
        self.setup_ui()
        self.start_new_game()
        self.center_window()
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.start_new_game())
        self.root.bind('<F1>', lambda e: self.give_hint())
    
    def setup_ui(self):
        # Colors
        colors = {"bg": "#2C3E50", "btn": "#3498DB", "text": "#ECF0F1", 
                 "success": "#2ECC71", "error": "#E74C3C", "warning": "#F39C12"}
        
        # Title
        tk.Label(self.root, text="🎯 Number Guessing Game", font=("Arial", 20, "bold"),
                bg=colors["bg"], fg=colors["text"]).pack(pady=10)
        
        # Game info
        self.info_label = tk.Label(self.root, font=("Arial", 11), bg=colors["bg"], fg=colors["text"])
        self.info_label.pack()
        
        # Difficulty
        diff_frame = tk.Frame(self.root, bg=colors["bg"])
        diff_frame.pack(pady=5)
        tk.Label(diff_frame, text="Difficulty:", bg=colors["bg"], fg=colors["text"]).pack(side=tk.LEFT)
        self.diff_var = tk.StringVar(value=self.difficulty)
        for diff in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(diff_frame, text=diff, variable=self.diff_var, 
                          value=diff.lower(), bg=colors["bg"], fg=colors["text"],
                          command=self.change_difficulty).pack(side=tk.LEFT, padx=5)
        
        # Stats display
        stats_frame = tk.Frame(self.root, bg=colors["bg"])
        stats_frame.pack(pady=5)
        self.attempts_label = tk.Label(stats_frame, font=("Arial", 11, "bold"),
                                      bg=colors["bg"], fg=colors["text"])
        self.attempts_label.pack(side=tk.LEFT, padx=10)
        self.score_label = tk.Label(stats_frame, font=("Arial", 11, "bold"),
                                   bg=colors["bg"], fg=colors["warning"])
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Input area
        input_frame = tk.Frame(self.root, bg=colors["bg"])
        input_frame.pack(pady=15)
        tk.Label(input_frame, text="Enter guess:", bg=colors["bg"], fg=colors["text"]).pack()
        self.guess_entry = tk.Entry(input_frame, font=("Arial", 20), width=10, justify='center')
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind('<Return>', lambda e: self.check_guess())
        
        # Guess button
        tk.Button(input_frame, text="Guess", command=self.check_guess, font=("Arial", 12),
                 bg=colors["btn"], fg="white", padx=20).pack(pady=5)
        
        # Feedback
        self.feedback_label = tk.Label(self.root, font=("Arial", 12, "bold"),
                                      bg=colors["bg"], wraplength=400)
        self.feedback_label.pack(pady=10)
        
        # History
        tk.Label(self.root, text="Recent Guesses:", bg=colors["bg"], fg=colors["text"]).pack()
        self.history_listbox = tk.Listbox(self.root, width=30, height=6, bg="#34495E", fg="white")
        self.history_listbox.pack(pady=5)
        
        # Control buttons
        btn_frame = tk.Frame(self.root, bg=colors["bg"])
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="New Game", command=self.start_new_game,
                 bg=colors["success"], fg="white", padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Hint", command=self.give_hint,
                 bg=colors["warning"], fg="white", padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Stats", command=self.show_stats,
                 bg="#9B59B6", fg="white", padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Quit", command=self.root.quit,
                 bg=colors["error"], fg="white", padx=15).pack(side=tk.LEFT, padx=5)
        
        self.guess_entry.focus()
    
    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def change_difficulty(self):
        self.difficulty = self.diff_var.get()
        self.start_new_game()
    
    def start_new_game(self):
        settings = self.difficulty_settings[self.difficulty]
        self.max_number = settings["max"]
        self.max_attempts = settings["attempts"]
        self.secret_number = random.randint(1, self.max_number)
        self.attempts = 0
        self.score = 100 * settings["multiplier"]
        self.game_active = True
        self.hints_used = 0
        
        self.info_label.config(text=f"Guess a number between 1 and {self.max_number}")
        self.attempts_label.config(text=f"Attempts: 0/{self.max_attempts}")
        self.score_label.config(text=f"Score: {int(self.score)}")
        self.feedback_label.config(text="New game started!", fg="#ECF0F1")
        self.history_listbox.delete(0, tk.END)
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        
        self.stats["games_played"] += 1
    
    def check_guess(self):
        if not self.game_active:
            return
        
        guess_text = self.guess_entry.get()
        if not guess_text:
            messagebox.showwarning("Input needed", "Enter a number!")
            return
        
        try:
            guess = int(guess_text)
            if guess < 1 or guess > self.max_number:
                messagebox.showwarning("Invalid", f"Enter 1-{self.max_number}")
                return
            
            self.attempts += 1
            self.score = max(0, self.score - 10)
            
            if guess < self.secret_number:
                feedback = f"{guess} - Too low!"
                color = "#3498DB"
                icon = "🔽"
            elif guess > self.secret_number:
                feedback = f"{guess} - Too high!"
                color = "#3498DB"
                icon = "🔼"
            else:
                feedback = f"{guess} - CORRECT! 🎉"
                color = "#2ECC71"
                icon = "✅"
                self.game_active = False
                self.stats["games_won"] += 1
                self.stats["streak"] += 1
                if self.score > self.stats["best_score"]:
                    self.stats["best_score"] = int(self.score)
                
                messagebox.showinfo("You Win!", 
                    f"Number: {self.secret_number}\nAttempts: {self.attempts}\nScore: {int(self.score)}")
                self.save_to_leaderboard()
            
            # Update display
            self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
            self.score_label.config(text=f"Score: {int(self.score)}")
            self.feedback_label.config(text=feedback, fg=color)
            self.history_listbox.insert(0, f"#{self.attempts}: {guess} {icon}")
            
            if guess != self.secret_number and self.attempts >= self.max_attempts:
                self.game_active = False
                messagebox.showinfo("Game Over", f"The number was {self.secret_number}")
                self.stats["streak"] = 0
            
            self.guess_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number!")
            self.guess_entry.delete(0, tk.END)
    
    def give_hint(self):
        if not self.game_active:
            messagebox.showinfo("Game Over", "Start a new game!")
            return
        
        self.hints_used += 1
        self.score = max(0, self.score - 15)
        
        hints = [
            f"The number is {'even' if self.secret_number % 2 == 0 else 'odd'}",
            f"The number is {'>50' if self.secret_number > 50 else '≤50'}",
            f"Sum of digits: {sum(int(d) for d in str(self.secret_number))}",
            f"Within 20 of: {random.randint(max(1, self.secret_number-20), min(self.max_number, self.secret_number+20))}"
        ]
        
        hint = random.choice(hints[:min(self.hints_used, len(hints))])
        self.feedback_label.config(text=f"💡 Hint: {hint}", fg="#F39C12")
        self.score_label.config(text=f"Score: {int(self.score)}")
    
    def load_leaderboard(self):
        try:
            if os.path.exists("leaderboard.json"):
                with open("leaderboard.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_to_leaderboard(self):
        name = simpledialog.askstring("Save Score", "Your name:", parent=self.root) or "Player"
        entry = {
            "name": name, 
            "score": int(self.score), 
            "attempts": self.attempts,
            "difficulty": self.difficulty,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.leaderboard.append(entry)
        self.leaderboard.sort(key=lambda x: -x["score"])
        self.leaderboard = self.leaderboard[:10]
        
        try:
            with open("leaderboard.json", "w") as f:
                json.dump(self.leaderboard, f, indent=2)
        except:
            pass
    
    def show_stats(self):
        games = self.stats["games_played"]
        wins = self.stats["games_won"]
        win_rate = (wins/games*100) if games > 0 else 0
        
        stats_text = f"""📊 Statistics 📊
        
Games Played: {games}
Games Won: {wins}
Win Rate: {win_rate:.1f}%
Current Streak: {self.stats['streak']}
Best Score: {self.stats['best_score']}

Current Game:
Difficulty: {self.difficulty.capitalize()}
Range: 1-{self.max_number}
Max Attempts: {self.max_attempts}
        """
        messagebox.showinfo("Game Statistics", stats_text)

def main():
    root = tk.Tk()
    game = EnhancedGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()