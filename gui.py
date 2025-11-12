import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


def translation(x, y, z):
    t_matrix = np.identity(4)
    t_matrix[0, 3] = x
    t_matrix[1, 3] = y
    t_matrix[2, 3] = z
    return t_matrix


def create_rotation_matrix_x(angle_deg):
    rad = np.radians(angle_deg)
    c = np.cos(rad)
    s = np.sin(rad)
    rx_matrix = np.identity(4)
    rx_matrix[1, 1] = c
    rx_matrix[1, 2] = -s
    rx_matrix[2, 1] = s
    rx_matrix[2, 2] = c
    return rx_matrix


def create_rotation_matrix_y(angle_deg):
    rad = np.radians(angle_deg)
    c = np.cos(rad)
    s = np.sin(rad)
    ry_matrix = np.identity(4)
    ry_matrix[0, 0] = c
    ry_matrix[0, 2] = s
    ry_matrix[2, 0] = -s
    ry_matrix[2, 2] = c
    return ry_matrix


def create_rotation_matrix_z(angle_deg):
    rad = np.radians(angle_deg)
    c = np.cos(rad)
    s = np.sin(rad)
    rz_matrix = np.identity(4)
    rz_matrix[0, 0] = c
    rz_matrix[0, 1] = -s
    rz_matrix[1, 0] = s
    rz_matrix[1, 1] = c
    return rz_matrix


def calculate_concatennation_r(rx, ry, rz):
    # Order: rz @ ry @ rx
    return rz @ ry @ rx


def transformation_matrix(crm, tm):
    tr_matrix = np.identity(4)
    tr_matrix[0:3, 0:3] = crm[0:3, 0:3]
    tr_matrix[0:3, 3] = tm[0:3, 3]
    return tr_matrix


def matrix_to_text(mat):
    return np.array2string(mat, formatter={'float_kind':lambda x: f"{x:8.4f}"})


class TransformGUI:
    def _apply_style(self):
        s = ttk.Style()
        try:
            s.theme_use('clam')
        except Exception:
            pass

        # colors
        bg = '#f4f7fb'        # window background
        card = '#ffffff'      # card/frame background
        accent = '#2b8aef'    # primary accent color
        entry_bg = '#ffffff'
        text_bg = '#0b1220'
        text_fg = '#e6eef6'

        try:
            self.root.configure(bg=bg)
        except Exception:
            pass

        s.configure('Card.TFrame', background=card)
        s.configure('Card.TLabel', background=card, font=('Segoe UI', 10))
        s.configure('Card.TEntry', fieldbackground=entry_bg, background=entry_bg, padding=6)

        s.configure('Accent.TButton', background=accent, foreground='white', font=('Segoe UI', 10), padding=6)
        s.map('Accent.TButton', background=[('active', '#1f6fbf')])

        s.configure('Tool.TButton', relief='flat', padding=6, font=('Segoe UI', 10))

        try:
            self._st_bg = text_bg
            self._st_fg = text_fg
        except Exception:
            self._st_bg = '#0b1220'
            self._st_fg = '#e6eef6'

    def __init__(self, root):
        self.root = root
        root.title('Matrix Calculations')

        self._apply_style()

        frm = ttk.Frame(root, padding=(12, 12, 12, 12), style='Card.TFrame')
        frm.grid(row=0, column=0, sticky='nsew')

        # Translation inputs
        ttk.Label(frm, text='Translation (x, y, z):', style='Card.TLabel').grid(column=0, row=0, sticky='w')
        self.tx = tk.DoubleVar(value=0.0)
        self.ty = tk.DoubleVar(value=0.0)
        self.tz = tk.DoubleVar(value=0.0)
        ttk.Entry(frm, textvariable=self.tx, width=10, style='Card.TEntry').grid(column=1, row=0, padx=6)
        ttk.Entry(frm, textvariable=self.ty, width=10, style='Card.TEntry').grid(column=2, row=0, padx=6)
        ttk.Entry(frm, textvariable=self.tz, width=10, style='Card.TEntry').grid(column=3, row=0, padx=6)

        # Rotation inputs
        ttk.Label(frm, text='Rotation (deg) X, Y, Z:', style='Card.TLabel').grid(column=0, row=1, sticky='w', pady=(8, 0))
        self.rx = tk.DoubleVar(value=0.0)
        self.ry = tk.DoubleVar(value=0.0)
        self.rz = tk.DoubleVar(value=0.0)
        ttk.Entry(frm, textvariable=self.rx, width=10, style='Card.TEntry').grid(column=1, row=1, padx=6, pady=(8, 0))
        ttk.Entry(frm, textvariable=self.ry, width=10, style='Card.TEntry').grid(column=2, row=1, padx=6, pady=(8, 0))
        ttk.Entry(frm, textvariable=self.rz, width=10, style='Card.TEntry').grid(column=3, row=1, padx=6, pady=(8, 0))

        btn_frame = ttk.Frame(frm, style='Card.TFrame')
        btn_frame.grid(column=0, row=2, columnspan=4, pady=(12, 6), sticky='w')
        ttk.Button(btn_frame, text='Compute', command=self.compute, style='Accent.TButton').grid(column=0, row=0, padx=(0, 8))
        ttk.Button(btn_frame, text='Copy to Clipboard', command=self.copy_to_clipboard, style='Tool.TButton').grid(column=1, row=0, padx=(0, 8))
        ttk.Button(btn_frame, text='Clear', command=self.clear, style='Tool.TButton').grid(column=2, row=0)

        self.out = ScrolledText(frm, width=72, height=18, bd=0, relief='flat', bg=self._st_bg, fg=self._st_fg, insertbackground=self._st_fg)
        self.out.grid(column=0, row=3, columnspan=4, pady=(8, 0))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.last_text = ''

    def compute(self):
        tm = translation(self.tx.get(), self.ty.get(), self.tz.get())
        rxm = create_rotation_matrix_x(self.rx.get())
        rym = create_rotation_matrix_y(self.ry.get())
        rzm = create_rotation_matrix_z(self.rz.get())
        crm = calculate_concatennation_r(rxm, rym, rzm)
        tr_m = transformation_matrix(crm, tm)
        try:
            inv = np.linalg.inv(tr_m)
        except np.linalg.LinAlgError:
            inv = None

        out_lines = []
        out_lines.append('Translation matrix (4x4): ')
        out_lines.append(matrix_to_text(tm))
        out_lines.append('\n')

        out_lines.append('Rotation Matrix X (4x4): ')
        out_lines.append(matrix_to_text(rxm))
        out_lines.append('\n')

        out_lines.append('Rotation Matrix Y (4x4): ')
        out_lines.append(matrix_to_text(rym))
        out_lines.append('\n')
        
        out_lines.append('Rotation Matrix Z (4x4): ')
        out_lines.append(matrix_to_text(rzm))
        out_lines.append('\n')

        out_lines.append('Transformation matrix (4x4):')
        out_lines.append(matrix_to_text(tr_m))
        out_lines.append('\n')

        if inv is None:
            out_lines.append('Inverse: (matrix is singular, no inverse)')
        else:
            out_lines.append('Inverse matrix (4x4):')
            out_lines.append(matrix_to_text(inv))

        text = '\n'.join(out_lines)
        self.last_text = text
        self.out.delete('1.0', tk.END)
        self.out.insert(tk.END, text)

    def clear(self):
        self.tx.set(0.0)
        self.ty.set(0.0)
        self.tz.set(0.0)
        self.rx.set(0.0)
        self.ry.set(0.0)
        self.rz.set(0.0)
        self.last_text = ''
        self.out.delete('1.0', tk.END)
        try:
            for child in self.root.winfo_children():
                child.focus()
                break
        except Exception:
            pass

    def copy_to_clipboard(self):
        if self.last_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.last_text)
            self.root.update()  
def main():
    root = tk.Tk()
    app = TransformGUI(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
