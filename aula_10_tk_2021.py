from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.msg = Label(self, text="Hello World")
        self.msg.pack ()
        self.bye = Button (self, text="Bye", command=master.destroy)
        self.bye.pack ()
        self.pack()
        
##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    master.geometry("640x480+0+0")
##    app = Application(master)
##    mainloop()


class Exemplo2(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.rotulo = Label(self, text="Exemplo", foreground="blue")
##        self.rotulo.pack()
        self.rotulo.configure(relief="sunken", font="Arial 24 bold", border=5,\
                              background="yellow")
        print(self.rotulo.cget("relief"))
        self.pack()

##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    master.geometry("640x480+0+0")
##    app = Exemplo2(master)
##    mainloop()


class Exemplo3(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        a = Label (self, text="A")
        a.pack (side="left")
        b = Label (self, text="B")
        b.pack (side="bottom")
        c = Label (self, text="C")
        c.pack (side="right")
        d = Label (self, text="D")
        d.pack (side="top")
        for widget in (a,b,c,d):
            widget.configure(relief="groove", border=10, font="Times 24 bold")
        self.pack()
        
##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    app = Exemplo3(master)
##    mainloop()

class Exemplo4(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        a = Label (self, text="A")
        a.pack (side="left", fill='y')
        b = Label (self, text="B")
        b.pack (side="bottom", fill='x')
        c = Label (self, text="C")
        c.pack (side="right", fill='both')
        d = Label (self, text="D")
        d.pack (side="top", fill='both')
        for widget in (a,b,c,d):
            widget.configure(relief="groove", border=10, font="Times 24 bold")
        self.pack(expand=True, fill='both')

##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    master.geometry("640x480+0+0")
##    app = Exemplo4(master)
##    mainloop()

class Exemplo5(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        a = Label (self, text="A")
        a.pack (side="left", fill='y', expand=True)
        b = Label (self, text="B")
        b.pack (side="bottom", fill='x', expand=True)
        c = Label (self, text="C")
        c.pack (side="right", fill='both')
        d = Label (self, text="D")
        d.pack (side="top", fill='both')
        for widget in (a,b,c,d):
            widget.configure(relief="groove", border=10, font="Times 24 bold")
        self.pack(expand=True, fill='both')

##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    app = Exemplo5(master)
##    mainloop()


class Exemplo6(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        top = Frame(self)
        top.pack(fill='x')
        
        a = Label (top, text="A")
        b = Label (top, text="B")
        c = Label (top, text="C")
        d = Label (top, text="D")
        for widget in (a,b,c,d):
            widget.configure(relief="groove", border=10, font="Times 24 bold")
            widget.pack (side="left", fill='both', expand=True)
            
        self.pack(expand=True, fill='both')

##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    app = Exemplo6(master)
##    mainloop()

class Exemplo7(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        top = Frame(self)
        top.pack(fill='x')
        
        a = Label (top, text="A")
        b = Label (top, text="B")
        c = Label (top, text="C")
        d = Label (self, text="D")
        for widget in (a,b,c,d):
            widget.configure(relief="groove", border=10, font="Times 24 bold")
            widget.pack (side="left", fill='both', expand=True)
            
        self.pack(expand=True, fill='both')

##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    app = Exemplo7(master)
##    mainloop()

class Exemplo8:
    def __init__(self, master):
        self.b = Button(master, text="+", command=self.inc)
        self.b2 = Button(master, text="-", command=self.dec)
        self.rotulo = Label(master, text="0")
        self.rotulo.pack()
        self.b.pack()
        self.b2.pack()
        self.rotulo.pack()

    def inc(self):
        n = int(self.rotulo.cget("text"))
        n += 1
        self.rotulo.configure(text=str(n))

    def dec(self):
        n = int(self.rotulo.cget("text"))
        n -= 1
        self.rotulo.configure(text=str(n))
    
##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    app = Exemplo8(master)
##    mainloop()

class Exemplo9:
    def __init__(self, master):
        self.rotulo = Label(master)
        self.rotulo.pack(expand=True, fill='both')
        self.rotulo.bind("<Button-1>", self.clica)
        self.rotulo.bind("<Key>", self.tecla)
        
    def clica(self, evento):
        txt = "Mouse clicado em {0}x{1}\n {2}x{3}".format(evento.x, evento.y,\
                                                          evento.x_root, evento.y_root)
        self.rotulo.configure(text=txt)
        self.rotulo.focus()

    def tecla(self, e):
        txt="Keysym={0}\nKeycode={1}\nChar={2}".format(e.keysym,\
                                                       e.keycode,e.char)
        e.widget.configure(text=txt)


##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    master.geometry("640x480+0+0")
##    app = Exemplo9(master)
##    mainloop()


class Exemplo10:
    def __init__(self, master):
        principal = Menu(master)
        arquivo = Menu(principal, tearoff=0)
        arquivo.add_command(label="Abrir", command=self.abrir)
        arquivo.add_command(label="Salvar", command=self.salvar)
        principal.add_cascade(label="Arquivo", menu=arquivo)
        principal.add_command(label="Ajuda", command=self.ajuda)
        master.configure(menu=principal)

    def abrir(self):
        print("Abrir")

    def salvar(self):
        print("Salvar")

    def ajuda(self):
        print("Ajuda")
        
##if __name__ == '__main__':
##    master = Tk()
##    master.title("Exemplo")
##    master.geometry("640x480+0+0")
##    app = Exemplo10(master)
##    mainloop()

class exemplo_popup(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.menu = Menu(self.master, tearoff=0)
        self.menu.add_command(label="Salvar", command=self.salvar)
        self.menu.add_command(label="Ajuda", command=self.ajuda)
        self.frame = Frame(self.master, width=200, height=200)
        self.frame.pack(expand=True, fill='both')
        self.frame.bind("<Button-3>", self.popup)
        
    def salvar(self):
        print("salvar")
        
    def ajuda(self):
        print("ajuda")
        
    def popup(self, e):
        self.menu.tk_popup(e.x_root, e.y_root)
        
##if __name__ == '__main__':
##    master=Tk()
##    app = exemplo_popup(master)
##    mainloop() 


class exemplo_entry(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.label = Label(self.master, text='Email')
        self.label.pack()
        self.e = Entry(self.master, font="Arial 24")
        self.i = Button(self.master, text="Insere @",command=self.insere)
        self.l = Button(self.master, text="Limpa",command=self.limpa)
        self.e.pack()
        for w in (self.i,self.l):
            w.pack(side='left')

    def insere(self):
        self.e.insert(INSERT,"@")
    def limpa(self):
        self.e.delete(0,END)
##if __name__ == '__main__':
##    master=Tk()
##    master.geometry("400x300")
##    app = exemplo_entry(master)
##    mainloop()

class exemplo_var(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.soma = DoubleVar(self.master)
        self.parcela = DoubleVar(self.master)
        self.lsoma = Label(self.master, textvar=self.soma)
        self.eparcela = Entry(self.master, textvar=self.parcela)
        self.eparcela.bind("<Return>", self.aritmetica)
        self.eparcela.bind("<KP_Enter>", self.aritmetica)
        self.lsoma.pack()
        self.eparcela.pack()
    def aritmetica(self, e):
        self.soma.set(self.soma.get() + self.parcela.get())
        
if __name__ == '__main__':
    master=Tk()
    app = exemplo_var(master)
    mainloop()

