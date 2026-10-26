import tkinter as tk
from tkinter import messagebox
import json
import os

GREEN = "#53FC18"
BG = "#101010"
PANEL = "#202020"


class KickTool:
    def __init__(self, root):
        self.root = root
        self.root.title("KICK CHAT TOOL PRO")
        self.root.geometry("650x750")
        self.root.configure(bg=BG)

        self.running = False
        self.sent = 0
        self.accounts = []

        self.load_accounts()
        self.create_ui()

    def label(self, text, size=12, color="white"):
        return tk.Label(
            self.root,
            text=text,
            font=("Arial", size, "bold"),
            bg=BG,
            fg=color
        )

    def entry(self):
        e = tk.Entry(
            self.root,
            bg=PANEL,
            fg="white",
            insertbackground="white",
            font=("Arial", 12),
            relief="flat",
            justify="center"
        )
        e.pack(padx=50, pady=5, fill="x", ipady=6)
        return e

    def create_ui(self):
        self.label(
            "KICK CHAT TOOL PRO",
            24,
            GREEN
        ).pack(pady=15)

        self.label("ACCOUNT MANAGER").pack()

        self.account_entry = self.entry()

        tk.Button(
            self.root,
            text="+ ADD ACCOUNT",
            command=self.add_account,
            bg=GREEN,
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        self.account_list = tk.Listbox(
            self.root,
            height=4,
            bg=PANEL,
            fg=GREEN,
            relief="flat"
        )
        self.account_list.pack(
            padx=50,
            pady=5,
            fill="x"
        )

        self.refresh_accounts()

        tk.Button(
            self.root,
            text="REMOVE ACCOUNT",
            command=self.remove_account,
            bg="#ff5555"
        ).pack(pady=5)

        self.label("CHANNEL USERNAME").pack()
        self.channel = self.entry()

        self.label("MESSAGE").pack()
        self.message = self.entry()

        self.label("MESSAGE COUNT").pack()
        self.count = self.entry()
        self.count.insert(0, "10")

        self.label("DELAY (SECONDS)").pack()
        self.delay = self.entry()
        self.delay.insert(0, "5")

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(pady=15)

        tk.Button(
            frame,
            text="▶ START",
            command=self.start,
            bg=GREEN,
            width=15
        ).pack(side="left", padx=10)

        tk.Button(
            frame,
            text="■ STOP",
            command=self.stop,
            bg="#ff5555",
            width=15
        ).pack(side="left", padx=10)

        self.status = self.label(
            "STATUS: READY",
            12,
            GREEN
        )
        self.status.pack()

        self.counter = self.label("SENT: 0")
        self.counter.pack()

        self.log = tk.Text(
            self.root,
            height=8,
            bg=PANEL,
            fg=GREEN
        )
        self.log.pack(
            padx=30,
            pady=10,
            fill="both"
        )

        self.log.insert(
            "end",
            "KICK TOOL READY\nMODE: SIMULATION\n"
        )

    def add_account(self):
        name = self.account_entry.get().strip()

        if not name:
            return

        if name not in self.accounts:
            self.accounts.append(name)
            self.save_accounts()
            self.refresh_accounts()

        self.account_entry.delete(0, "end")

    def remove_account(self):
        selection = self.account_list.curselection()

        if selection:
            self.accounts.pop(selection[0])
            self.save_accounts()
            self.refresh_accounts()

    def refresh_accounts(self):
        self.account_list.delete(0, "end")

        for account in self.accounts:
            self.account_list.insert(
                "end",
                f"● {account}"
            )

    def save_accounts(self):
        with open(
            "accounts.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(self.accounts, f)

    def load_accounts(self):
        if os.path.exists("accounts.json"):
            try:
                with open(
                    "accounts.json",
                    "r",
                    encoding="utf-8"
                ) as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.accounts = [
                            x for x in data
                            if isinstance(x, str)
                        ]
            except (OSError, ValueError):
                self.accounts = []

    def start(self):
        if self.running:
            return

        channel = self.channel.get().strip()
        message = self.message.get().strip()

        if not channel or not message:
            messagebox.showerror(
                "Error",
                "Enter channel and message"
            )
            return

        if not self.accounts:
            messagebox.showerror(
                "Error",
                "Add an account first"
            )
            return

        try:
            self.total = int(self.count.get())
            self.delay_seconds = float(self.delay.get())

            if not 1 <= self.total <= 1000:
                raise ValueError

            if not 0.1 <= self.delay_seconds <= 3600:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid count or delay"
            )
            return

        self.running = True
        self.sent = 0

        self.channel_name = channel
        self.message_text = message

        self.status.config(text="STATUS: RUNNING")
        self.send()

    def send(self):
        if not self.running:
            return

        if self.sent >= self.total:
            self.running = False
            self.status.config(text="STATUS: COMPLETED")
            return

        account = self.accounts[
            self.sent % len(self.accounts)
        ]

        self.sent += 1

        self.log.insert(
            "end",
            f"[SIMULATION] @{account} -> "
            f"{self.channel_name}: "
            f"{self.message_text}\n"
        )

        self.log.see("end")

        self.counter.config(
            text=f"SIMULATED: {self.sent}/{self.total}"
        )

        if self.sent >= self.total:
            self.running = False
            self.status.config(text="STATUS: COMPLETED")
        else:
            self.root.after(
                int(self.delay_seconds * 1000),
                self.send
            )

    def stop(self):
        self.running = False
        self.status.config(text="STATUS: STOPPED")


if __name__ == "__main__":
    root = tk.Tk()
    app = KickTool(root)
    root.mainloop()
