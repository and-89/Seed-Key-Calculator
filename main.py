import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ctypes

class SeedKeyApp:
    def __init__(self, master):
        self.master = master
        self.master.iconbitmap('logo.ico')
        master.title('Seed & Key Calculator')
        master.geometry("600x400")  # Increase window size

        # Styling
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12), background='lightgray')
        self.style.configure('Success.TButton', background='light green', foreground='green')

        # Main frame
        self.frame = ttk.Frame(master, padding="10 10 10 10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.seed_var = tk.StringVar()
        self.key_var = tk.StringVar()

        ttk.Label(self.frame, text="Seed (hex):").grid(column=0, row=0, sticky=tk.W)
        self.seed_entry = ttk.Entry(self.frame, textvariable=self.seed_var, font=('Arial', 11), width=1)
        self.seed_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        self.load_button = ttk.Button(self.frame, text="Load DLL", command=self.load_dll)
        self.load_button.grid(column=0, row=1, sticky=tk.W, pady=5)

        self.calculate_button = ttk.Button(self.frame, text="Calculate Key", command=self.calculate_key)
        self.calculate_button.grid(column=1, row=1, sticky=tk.W, pady=5)

        ttk.Label(self.frame, text="Key:").grid(column=0, row=2, sticky=tk.W)
        self.key_entry = ttk.Entry(self.frame, textvariable=self.key_var, state='readonly', font=('Arial', 12), width=30)
        self.key_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)

        # Allows for flexible column scaling
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.dll = None

    def load_dll(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                self.dll = ctypes.WinDLL(filepath)
                self.load_button.configure(style='Success.TButton')  # Change button color to green after loading
                messagebox.showinfo("Success", "DLL has been loaded successfully.")
            except OSError as e:
                messagebox.showerror("Error", f"Failed to load DLL: {e}")
        else:
            messagebox.showinfo("Information", "DLL loading was cancelled.")

    def calculate_key(self):
        if self.seedkey and self.seed_entry.get():
            seed_hex = self.seed_entry.get()
            seed = [int(seed_hex[i:i + 2], 16) for i in range(0, len(seed_hex), 2)]
            key = self.compute_key_from_seed(seed)
            if key:
                self.key_entry.config(state='normal')
                self.key_entry.delete(0, tk.END)
                self.key_entry.insert(0, ''.join(key))
                self.key_entry.config(state='readonly')
            else:
                messagebox.showerror("Error", "Key calculation failed.")
        else:
            messagebox.showerror("Error", "DLL not loaded or seed not provided.")

    def compute_key_from_seed(self, seed):
        seed_array = (ctypes.c_ubyte * len(seed))(*seed)
        size_seed = len(seed)

        max_size_key = 4
        key_buffer = (ctypes.c_ubyte * max_size_key)()
        size_key = ctypes.c_ushort()

        result = self.ASAP1A_CCP_ComputeKeyFromSeed(seed_array, size_seed, key_buffer, max_size_key,
                                                    ctypes.byref(size_key))

        if result:
            key = [hex(byte)[2:].zfill(2) for byte in key_buffer[:size_key.value]]
            return key
        else:
            print("Error while calculating key")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SeedKeyApp(root)
    root.mainloop()
