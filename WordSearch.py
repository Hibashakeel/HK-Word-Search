import tkinter as tk
from tkinter import messagebox
import random
import os

def start_game():
    global score, selected_word, selected_coords, found_words, current_words, word_locations, grid
    score = 0
    selected_word = ""
    selected_coords = []
    found_words = []
    selected_level = level_var.get()
    current_words = get_words_for_level(selected_level)
    word_list_box.delete(0, tk.END)
    for word in current_words:
        word_list_box.insert(tk.END, word)
    generate_word_grid()
    update_score()
    skip_button.config(state=tk.NORMAL)

def get_words_for_level(level):
    if level == "Easy":
        return random.sample(easy_words, 3)
    elif level == "Medium":
        return random.sample(medium_words, 4)
    elif level == "Hard":
        return random.sample(hard_words, 5)
    return []

def generate_word_grid():
    global word_locations, grid
    for widget in grid_frame.winfo_children():
        widget.destroy()

    grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
    word_locations = []

    for word in current_words:
        place_word_in_grid(word)

    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] == "":
                grid[r][c] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            label = tk.Label(grid_frame, text=grid[r][c], borderwidth=1, relief="solid", width=2, height=1, bg="#ffffff", fg="black", font=('Arial', 12))
            label.grid(row=r, column=c)
            label.bind("<Button-1>", lambda e, row=r, col=c: letter_clicked(row, col))

def place_word_in_grid(word):
    global word_locations, grid
    word_len = len(word)
    placed = False
    while not placed:
        direction = random.choice(["H", "V", "D"])
        if direction == "H":
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - word_len)
        elif direction == "V":
            row = random.randint(0, grid_size - word_len)
            col = random.randint(0, grid_size - 1)
        elif direction == "D":
            row = random.randint(0, grid_size - word_len)
            col = random.randint(0, grid_size - word_len)

        if can_place_word(word, row, col, direction):
            word_locations.append((word, row, col, direction))
            for i in range(word_len):
                if direction == "H":
                    grid[row][col + i] = word[i]
                elif direction == "V":
                    grid[row + i][col] = word[i]
                elif direction == "D":
                    grid[row + i][col + i] = word[i]
            placed = True

def can_place_word(word, row, col, direction):
    for i in range(len(word)):
        if direction == "H" and grid[row][col + i] != "":
            return False
        elif direction == "V" and grid[row + i][col] != "":
            return False
        elif direction == "D" and grid[row + i][col + i] != "":
            return False
    return True

def update_score():
    score_label.config(text=f"Score: {score}")
    high_score_label.config(text=f"Highest Score: {high_scores[level_var.get()]} (Player: {high_score_players[level_var.get()]})")

def save_high_score():
    try:
        with open("high_score.txt", "w") as file:
            for level in levels:
                file.write(f"{high_scores[level]}\n")
                file.write(f"{high_score_players[level]}\n")
    except PermissionError as e:
        messagebox.showerror("Error", f"Permission denied: {e}")

def load_high_score():
    global high_scores, high_score_players
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            lines = file.readlines()
            for i, level in enumerate(levels):
                if i * 2 + 1 < len(lines):
                    high_scores[level] = int(lines[i * 2].strip())
                    high_score_players[level] = lines[i * 2 + 1].strip()
        update_score()

def skip_game():
    for word, row, col, direction in word_locations:
        for i in range(len(word)):
            if direction == "H":
                label = grid_frame.grid_slaves(row=row, column=col + i)[0]
            elif direction == "V":
                label = grid_frame.grid_slaves(row=row + i, column=col)[0]
            elif direction == "D":
                label = grid_frame.grid_slaves(row=row + i, column=col + i)[0]
            label.config(bg="yellow")
    update_score()
    messagebox.showinfo("Skipped", "All words have been highlighted.")
    skip_button.config(state=tk.DISABLED)

def letter_clicked(row, col):
    global selected_word, selected_coords, score, high_scores, high_score_players
    letter = grid[row][col]
    if (row, col) in selected_coords:
        # Deselect the letter if already selected
        selected_coords.remove((row, col))
        selected_word = selected_word[:-1]
        grid_frame.grid_slaves(row=row, column=col)[0].config(bg="#ffffff")
    else:
        # Select the letter
        selected_word += letter
        selected_coords.append((row, col))
        highlight_selection()

    if selected_word in current_words:
        found_words.append(selected_word)
        current_words.remove(selected_word)
        highlight_found_word()
        update_word_list()
        selected_word = ""
        selected_coords = []
        score += 1
        if score > high_scores[level_var.get()]:
            high_scores[level_var.get()] = score
            high_score_players[level_var.get()] = user_name.get()
            save_high_score()
        update_score()
        if not current_words:
            messagebox.showinfo("Congratulations!", "You found all the words! Level Completed.")
            skip_button.config(state=tk.DISABLED)

def highlight_selection():
    for row, col in selected_coords:
        label = grid_frame.grid_slaves(row=row, column=col)[0]
        label.config(bg="lightblue")

def highlight_found_word():
    for row, col in selected_coords:
        label = grid_frame.grid_slaves(row=row, column=col)[0]
        label.config(bg="lightgreen")

def update_word_list():
    word_list_box.delete(0, tk.END)
    for word in current_words:
        word_list_box.insert(tk.END, word)
    for word in found_words:
        word_list_box.insert(tk.END, word + " (found)")

root = tk.Tk()
root.title("Word Search Game")
root.configure(bg='#add8e6')  # Light blue background

user_name = tk.StringVar()
user_name.set("Player")
score = 0
high_scores = {"Easy": 0, "Medium": 0, "Hard": 0}
high_score_players = {"Easy": "None", "Medium": "None", "Hard": "None"}
current_words = []
grid_size = 10
easy_words = ["CAT", "DOG", "COW"]
medium_words = ["HORSE", "TIGER", "LION", "DEER"]
hard_words = ["DONKEY", "GIRAFFE", "ELEPHANT", "TURTLE", "MONKEY"]
word_locations = []
selected_coords = []
found_words = []
levels = ["Easy", "Medium", "Hard"]

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# User name input
tk.Label(root, text="Enter your name:", bg='#add8e6', font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=5, padx=5, sticky="e")
tk.Entry(root, textvariable=user_name, font=('Arial', 12)).grid(row=0, column=1, pady=5, padx=5, sticky="w")

# Level selection
tk.Label(root, text="Select Level:", bg='#add8e6', font=('Arial', 12, 'bold')).grid(row=1, column=0, pady=5, padx=5, sticky="e")
level_var = tk.StringVar(value="Easy")
tk.OptionMenu(root, level_var, *levels).grid(row=1, column=1, pady=5, padx=5, sticky="w")

# Start button
tk.Button(root, text="Start Game", command=start_game, bg='#4caf50', fg='white', font=('Arial', 12, 'bold')).grid(row=2, column=0, columnspan=2, pady=10)

# Score display
score_label = tk.Label(root, text="Score: 0", bg='#add8e6', font=('Arial', 12, 'bold'))
score_label.grid(row=3, column=0, columnspan=2, pady=5)

# Highest score display
high_score_label = tk.Label(root, text="Highest Score: 0 (Player: None)", bg='#add8e6', font=('Arial', 12, 'bold'))
high_score_label.grid(row=4, column=0, columnspan=2, pady=5)

# Word grid
grid_frame = tk.Frame(root, bg='#add8e6')
grid_frame.grid(row=5, column=0, columnspan=2, pady=10)

# Word list display
word_list_label = tk.Label(root, text="Words to find:", bg='#add8e6', font=('Arial', 12, 'bold'))
word_list_label.grid(row=0, column=2, padx=10)
word_list_box = tk.Listbox(root, font=('Arial', 12))
word_list_box.grid(row=1, column=2, rowspan=5, padx=10)

# Skip button
skip_button = tk.Button(root, text="Skip", command=skip_game, state=tk.DISABLED, bg='#f44336', fg='white', font=('Arial', 12, 'bold'))
skip_button.grid(row=6, column=2, pady=10)

load_high_score()
root.mainloop()
