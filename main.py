import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Ingot:
    def __init__(self, name="Ferroboo"):
        self.name = name
        self.hardness = 50
        self.toughness = 50
        self.ductility = 50
        self.health = 100
        self.max_health = 100
        self.quench_count = 0

    def quench(self):
        if self.quench_count >= 3:
            self.health -= 20
            self.hardness -= 10
            self.toughness -= 15
            messagebox.showwarning("Critical Warning", 
                f"{self.name} is critically brittle! The metal is starting to fail and lose its properties!")
        else:
            self.hardness += 20
            self.toughness -= 10
            self.ductility -= 15
            messagebox.showinfo("Quenching", f"{self.name} has been quenched!")
            if self.hardness >= 120:
                messagebox.showwarning("Warning", 
                    f"{self.name} is getting brittle! You can only safely quench {3 - self.quench_count} more times.")
        
        self.quench_count += 1

        if self.ductility <=25:
            messagebox.showwarning("Warning", 
                f"{self.name} is losing ductility! Health reduced by 10.")
            self.health -= 10

    def temper(self):
        self.hardness += 5
        self.toughness += 10
        self.ductility += 10
        messagebox.showinfo("Tempering", f"{self.name} has been tempered!")

    def anneal(self):
        self.hardness -= 10
        self.toughness += 15
        self.ductility += 20
        messagebox.showinfo("Annealing", f"{self.name} has been annealed!")

    def restore_health(self):
        self.health = self.max_health

class Boss:
    def __init__(self, name, hardness, toughness, health, image_path):
        self.name = name
        self.hardness = hardness
        self.toughness = toughness
        self.health = health
        self.max_health = health
        self.image_path = image_path
        self.image = ImageTk.PhotoImage(Image.open(image_path))

    def restore_health(self):
        self.health = self.max_health

class FerrobooApp:
    def __init__(self, root):
        self.root = root 
        bg_image = Image.open("stage.png")  
        bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)  
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Set up the background label
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind('<Configure>', self.resize_background)

        self.ferroboo = Ingot()
        self.bosses = [
            Boss("Iron Crusher", hardness=60, toughness=40, health=120, image_path="iron_crusher.jpg"),
            Boss("Steel Knight", hardness=70, toughness=50, health=140, image_path="steel_samurai.jpg"),
            Boss("Titanium Terror", hardness=80, toughness=60, health=160, image_path="titanium_terror.jpg"),
            Boss("Diamond Destroyer", hardness=90, toughness=70, health=180, image_path="diamond_destroyer.jpg"),
            Boss("Adamantine Annihilator", hardness=100, toughness=80, health=200, image_path="adementium_wala.jpg"),
        ]
        self.current_boss_index = 0
        self.current_boss = self.bosses[self.current_boss_index]

        self.previous_stats = {
            "hardness": self.ferroboo.hardness,
            "toughness": self.ferroboo.toughness,
            "ductility": self.ferroboo.ductility,
            "health": self.ferroboo.health,
            "boss_health": self.current_boss.health
        }

        self.ferroboo_frame = tk.Frame(root, bg="#1E1E1E")
        self.ferroboo_frame.place(relx=0.32, rely=0.53, relwidth=0.09, relheight=0.17)

        self.boss_frame = tk.Frame(root, bg="#1E1E1E")
        self.boss_frame.place(relx=0.63, rely=0.53, relwidth=0.09, relheight=0.17)

        # Load and display Feroboo's image
        ferroboo_img = Image.open("feroboo_1.jpg").resize((160, 160), Image.LANCZOS)
        self.ferroboo_image = ImageTk.PhotoImage(ferroboo_img)
        self.ferroboo_label = tk.Label(self.ferroboo_frame, image=self.ferroboo_image, bg="#1E1E1E")
        self.ferroboo_label.pack()

        # Load and display the current boss's image
        self.update_boss_image()

        # Set up labels and log
        self.stats_label = tk.Label(root, text="", font=("Arial", 14), bg="#1E1E1E", fg="#FFFFFF")
        self.stats_label.pack()
        self.boss_stats_label = tk.Label(root, text="", font=("Arial", 14), bg="#1E1E1E", fg="#FF4D4D")
        self.boss_stats_label.pack()
        self.battle_log = tk.Text(root, height=10, width=50, font=("Arial", 10), bg="#2B2B2B", fg="#FFFFFF", wrap=tk.WORD)
        self.battle_log.pack()

        self.create_buttons()
        self.update_stats()

    def resize_background(self, event):
        bg_image = Image.open("stage.png")
        bg_image = bg_image.resize((event.width, event.height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        self.bg_label.config(image=self.bg_image)

    def create_buttons(self):
        self.treatment_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.treatment_frame.pack()
        
        self.quench_button = tk.Button(self.treatment_frame, text="Quenching", command=self.quench, bg="#007ACC", fg="#FFFFFF", font=("Arial", 12), activebackground="#005999")
        self.quench_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.temper_button = tk.Button(self.treatment_frame, text="Tempering", command=self.temper, bg="#00B3A4", fg="#FFFFFF", font=("Arial", 12), activebackground="#008B80")
        self.temper_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.anneal_button = tk.Button(self.treatment_frame, text="Annealing", command=self.anneal, bg="#FF8C00", fg="#FFFFFF", font=("Arial", 12), activebackground="#CC7000")
        self.anneal_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.battle_button = tk.Button(self.root, text="Battle with Boss", command=self.start_battle, bg="#FF4D4D", fg="#FFFFFF", font=("Arial", 14), activebackground="#CC3B3B")
        self.battle_button.pack(pady=10)

    def update_stats(self):
        arrow_up = "↑"
        arrow_down = "↓"

        def get_arrow(stat_name, current, previous):
            if current > previous:
                return f" {arrow_up} (+{current - previous})"
            elif current < previous:
                return f" {arrow_down} (-{previous - current})"
            else:
                return ""

        stats_text = (
            f"{self.ferroboo.name}'s Stats:\n"
            f"Hardness: {self.ferroboo.hardness}{get_arrow('hardness', self.ferroboo.hardness, self.previous_stats['hardness'])}\n"
            f"Toughness: {self.ferroboo.toughness}{get_arrow('toughness', self.ferroboo.toughness, self.previous_stats['toughness'])}\n"
            f"Ductility: {self.ferroboo.ductility}{get_arrow('ductility', self.ferroboo.ductility, self.previous_stats['ductility'])}\n"
            f"Health: {self.ferroboo.health}{get_arrow('health', self.ferroboo.health, self.previous_stats['health'])}\n"
            f"Quench Count: {self.ferroboo.quench_count}\n"
        )
        self.stats_label.config(text=stats_text)

        boss_stats_text = (
            f"Boss: {self.current_boss.name}\n"
            f"Hardness: {self.current_boss.hardness}\n"
            f"Toughness: {self.current_boss.toughness}\n"
            f"Health: {self.current_boss.health}{get_arrow('boss_health', self.current_boss.health, self.previous_stats['boss_health'])}\n"
        )
        self.boss_stats_label.config(text=boss_stats_text)

        self.previous_stats = {
            "hardness": self.ferroboo.hardness,
            "toughness": self.ferroboo.toughness,
            "ductility": self.ferroboo.ductility,
            "health": self.ferroboo.health,
            "boss_health": self.current_boss.health
        }


    def update_boss_image(self):
        boss_img = Image.open(self.current_boss.image_path).resize((160, 160), Image.LANCZOS)
        self.current_boss.image = ImageTk.PhotoImage(boss_img)
        if hasattr(self, 'boss_image_label'):
            self.boss_image_label.config(image=self.current_boss.image)
        else:
            self.boss_image_label = tk.Label(self.boss_frame, image=self.current_boss.image, bg="#1E1E1E")
            self.boss_image_label.grid(row=0, column=1, padx=(0, 0), sticky="e")

    def quench(self):
        self.ferroboo.quench()
        self.update_stats()

    def temper(self):
        self.ferroboo.temper()
        self.update_stats()

    def anneal(self):
        self.ferroboo.anneal()
        self.update_stats()

    def start_battle(self):
        self.battle_log.delete(1.0, tk.END)
        self.root.after(500, self.battle_round)

    def battle_round(self):
        if self.ferroboo.health > 0 and self.current_boss.health > 0:
            ingot_damage = max(self.ferroboo.hardness - self.current_boss.toughness, 0)
            boss_damage = max(self.current_boss.hardness - self.ferroboo.toughness, 0)
            self.current_boss.health -= ingot_damage
            self.ferroboo.health -= boss_damage

            round_text = (
                f"{self.ferroboo.name} dealt {ingot_damage} damage to {self.current_boss.name}! "
                f"{self.current_boss.name}'s Health: {self.current_boss.health}\n"
                f"{self.current_boss.name} dealt {boss_damage} damage to {self.ferroboo.name}! "
                f"{self.ferroboo.name}'s Health: {self.ferroboo.health}\n\n"
            )
            self.battle_log.insert(tk.END, round_text)
            self.update_stats()
            self.root.after(1000, self.battle_round)
        else:
            result = "Victory!" if self.ferroboo.health > 0 else f" Defeated by {self.bosses[self.current_boss_index].name}, Change your Strategy!\n"
            messagebox.showinfo("Battle Result", result)
            if self.ferroboo.health > 0:
                self.ferroboo.restore_health()
                self.current_boss.restore_health()
                self.current_boss_index += 1
                if self.current_boss_index < len(self.bosses):
                    self.current_boss = self.bosses[self.current_boss_index]
                    self.update_boss_image()
                    messagebox.showinfo("Next Battle", f"Prepare to face {self.current_boss.name}!")
                    self.update_stats()
                else:
                    messagebox.showinfo("Congratulations!", "You defeated all the bosses!" "You Are A Cheetah")
            else:
                self.ferroboo.restore_health()
                self.current_boss.restore_health()
                self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    app = FerrobooApp(root)
    root.mainloop()
