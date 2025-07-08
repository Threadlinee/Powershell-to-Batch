import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import os
import pyperclip
import time
from threading import Thread

def is_multiline(code):
    return "\n" in code.strip() or ";" in code

def convert_ps_to_bat(ps_code):
    if is_multiline(ps_code):
        bat_lines = [
            "@echo off",
            "set \"psScript=%TEMP%\\temp_script.ps1\"",
            "> \"%psScript%\" ("
        ]
        for line in ps_code.strip().splitlines():
            line = line.replace("%", "%%") 
            bat_lines.append(f"    echo {line}")
        bat_lines += [
            ")",
            "powershell -NoProfile -ExecutionPolicy Bypass -File \"%psScript%\"",
            "del \"%psScript%\" >nul 2>&1"
        ]
    else:
        escaped = ps_code.replace('"', '`"')
        bat_lines = [
            "@echo off",
            f"powershell -NoProfile -ExecutionPolicy Bypass -Command \"{escaped}\""
        ]
    return "\n".join(bat_lines)

def convert():
    ps_code = ps_input.get("1.0", tk.END).strip()
    if not ps_code:
        messagebox.showwarning("Warning", "Paste some PowerShell code first.")
        return
    bat_code = convert_ps_to_bat(ps_code)
    bat_output.delete("1.0", tk.END)
    animate_typing(bat_code)

def animate_typing(text):
    bat_output.delete("1.0", tk.END)
    def type_text():
        for char in text:
            bat_output.insert(tk.END, char)
            bat_output.see(tk.END)
            time.sleep(0.0015)
    Thread(target=type_text).start()

def copy_to_clipboard():
    code = bat_output.get("1.0", tk.END).strip()
    if code:
        pyperclip.copy(code)
        messagebox.showinfo("Copied", "Batch code copied to clipboard!")

def copy_input():
    code = ps_input.get("1.0", tk.END).strip()
    if code:
        pyperclip.copy(code)
        messagebox.showinfo("Copied", "PowerShell code copied to clipboard!")

def save_to_file():
    code = bat_output.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Nothing to save. Convert something first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".bat", filetypes=[("Batch Files", "*.bat")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(code)
        messagebox.showinfo("Saved", f"Batch file saved to:\n{file_path}")

def drop_handler(event):
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            code = f.read()
        ps_input.delete("1.0", tk.END)
        ps_input.insert(tk.END, code)

app = tk.Tk()
app.title("⚡ PS to BAT - Futuristic Converter")
app.geometry("1100x900")
app.config(bg="#000010")

try:
    app.tk.call('tkdnd::drop_target', 'register', app, '*')
    app.drop_target_register('*')
    app.dnd_bind('<<Drop>>', drop_handler)
except:
    pass

heading = tk.Label(app, text="⚡ PowerShell → Batch Converter", font=("Orbitron", 28, "bold"), bg="#000010", fg="#00ffff")
heading.pack(pady=25)

# PowerShell input
input_frame = tk.Frame(app, bg="#000010")
input_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 10), expand=True)

label_frame_top = tk.Frame(input_frame, bg="#000010")
label_frame_top.pack(fill=tk.X)

ps_label = tk.Label(label_frame_top, text="💻 PowerShell Code", bg="#000010", fg="#ffffff", font=("Consolas", 14, "bold"))
ps_label.pack(side=tk.LEFT)

copy_ps_btn = tk.Button(label_frame_top, text="📋 Copy", command=copy_input, bg="#4444aa", fg="white", font=("Orbitron", 10, "bold"))
copy_ps_btn.pack(side=tk.RIGHT, padx=6)

ps_input = scrolledtext.ScrolledText(input_frame, height=12, bg="#1a1a2e", fg="#00ff88", insertbackground="white", font=("Consolas", 12, "bold"), bd=3, relief=tk.FLAT)
ps_input.pack(fill=tk.BOTH, expand=True)

# Convert button
tk.Button(app, text="⚙️ Convert to .BAT", command=convert, bg="#ff0066", fg="white", padx=30, pady=14, font=("Orbitron", 14, "bold"), relief=tk.FLAT).pack(pady=25)

# Batch output
output_frame = tk.Frame(app, bg="#000010")
output_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 10), expand=True)

label_frame_bot = tk.Frame(output_frame, bg="#000010")
label_frame_bot.pack(fill=tk.X)

bat_label = tk.Label(label_frame_bot, text="📁 Batch Output", bg="#000010", fg="#ffffff", font=("Consolas", 14, "bold"))
bat_label.pack(side=tk.LEFT)

copy_btn = tk.Button(label_frame_bot, text="📋 Copy", command=copy_to_clipboard, bg="#4444aa", fg="white", font=("Orbitron", 10, "bold"))
copy_btn.pack(side=tk.RIGHT, padx=6)

save_btn = tk.Button(label_frame_bot, text="💾 Save", command=save_to_file, bg="#00aa66", fg="white", font=("Orbitron", 10, "bold"))
save_btn.pack(side=tk.RIGHT, padx=6)

bat_output = scrolledtext.ScrolledText(output_frame, height=12, bg="#1a1a2e", fg="#00ffff", insertbackground="white", font=("Consolas", 12, "bold"), bd=3, relief=tk.FLAT)
bat_output.pack(fill=tk.BOTH, expand=True)

# Footer
footer = tk.Label(app, text="made by 540sno 🧠 drag & drop .ps1 supported", bg="#000010", fg="#888888", font=("Orbitron", 10))
footer.pack(side=tk.BOTTOM, pady=10)

app.mainloop()
