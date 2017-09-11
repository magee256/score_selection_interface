import tkinter as tk


class Navbar(tk.Frame): ...
class Toolbar(tk.Frame ): ...
class Statusbar(tk.Frame): ...
class Main(tk.Frame): ...

class LoadRefDataWindow(tk.Frame):
    """
    This window is responsible for loading the full dataset of scores

    The user may load the data through a finder window or by drag and 
    drop. After data is loaded window transitions to LoadIDWindow
    """
    def __init__(self):
        super(LoadRefDataWindow,self).__init__()


class LoadIDWindow(tk.Frame):
    """
    This window is responsible for loading the student IDs we want data from

    The user may load the data through a finder window or by drag and 
    drop. 
    """

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainApplication,self).__init__()
        self.statusbar = Statusbar(self, ...)
        self.toolbar = Toolbar(self, ...)
        self.navbar = Navbar(self, ...)
        self.main = Main(self, ...)

        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
