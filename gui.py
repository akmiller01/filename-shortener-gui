import sys
from shorten import shorten
from tkinter import Label, Entry, Button, Tk, filedialog, END, Text, W, E, N, S, StringVar


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.configure(state='normal')
        self.text_space.insert('end', string)
        self.text_space.see('end')
        self.text_space.configure(state='disabled')

    def flush(self):
        pass


class Window:
    def __init__(self, master):
        self.input = None
        Label(root, text="Target directory").grid(row=1, column=0, sticky=W)
        Label(root, text="Target file length").grid(row=2, column=0, sticky=W)
        self.bart = Entry(master, state='disabled')
        self.bart.grid(row=1, column=1, sticky=W + E)
        barl_default_value = StringVar(root, value='256')
        self.barl = Entry(master, textvariable=barl_default_value)
        self.barl.grid(row=2, column=1, sticky=W + E)

        # Buttons
        self.tbutton = Button(root, text="Browse", command=self.browseinput)
        self.tbutton.grid(row=1, column=3, sticky=E)
        self.sbutton = Button(root, text="Shorten filenames", command=self.process)
        self.sbutton.grid(row=3, column=3, sticky=E)

        self.text_box = Text(root, wrap='word', height=10, state='disabled')
        self.text_box.grid(column=0, row=4, padx=5, pady=5, columnspan=4, sticky=W + E + N + S)
        sys.stdout = StdoutRedirector(self.text_box)
        sys.stderr = StdoutRedirector(self.text_box)

    def browseinput(self):
        Tk().withdraw()
        self.input = filedialog.askdirectory()
        self.bart.configure(state='normal')
        self.bart.delete(0, END)
        self.bart.insert(0, self.input)
        self.bart.configure(state='disabled')

    def process(self):
        if self.input:
            shorten(self.input, int(self.barl.get()))
        else:
            print("Error: Please select target directory.")


def on_closing():
    root.destroy()
    sys.exit(0)


root = Tk()
root.title("DevInit filename shortener")
root.protocol("WM_DELETE_WINDOW", on_closing)
window = Window(root)
root.mainloop()
