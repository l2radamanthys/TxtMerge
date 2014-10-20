

import Tkinter as tk
from tkFileDialog import askopenfilenames


class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.files = []

        self.pack()

        btn_select_files = tk.Button(self, text="Agregar Archivos", command=self.add_files)
        btn_select_files.grid(row=0, column=1)

        btn_up = tk.Button(self, text="Subir", command=self.move_up)
        btn_up.grid(row=1, column=2)
         
        btn_down = tk.Button(self, text="Bajar", command=self.move_down)
        btn_down.grid(row=2, column=2)
        
        btn_delete = tk.Button(self, text="Quitar", command=self.delete_item)
        btn_delete.grid(row=3, column=2)
        
        btn_clear = tk.Button(self, text="Limpiar", command=self.clear_list)
        btn_clear.grid(row=4, column=2)

        btn_merge = tk.Button(self, text="Unir Archivos")
        btn_merge.grid(row=5, column=1)



        self.file_list = tk.Listbox(self)
        self.file_list.grid(row=1, column=0, rowspan=4, columnspan=2)

        

    
    def add_files(self):
        """
            Agregar Archivos
        """
        files = askopenfilenames(multiple=True)
        for _file in files:
            fname = _file.split('/')[-1] 
            row = [fname, _file]
            if 1:#row in self.files: #no se permiten archivos duplicados
                self.files.append(row)
                self.file_list.insert(tk.END, fname)
                print fname


    
    def delete_item(self):
        try:
            pos = int(self.file_list.curselection()[0])
            self.file_list.delete(pos, pos)
            fname = self.file_list.get(pos)
            #falta eliminar el archivo de la lista interan
    
            print pos,fname
        except:
            pass


    def move_up(self):
        pos = int(self.file_list.curselection()[0])
        if pos != 0:
            fname = self.file_list.get(pos)
            self.file_list.delete(pos)
            self.file_list.insert(pos-1, fname)
            self.file_list.selection_set(pos-1)
            #falta mover el correspondiente en la lista interna


    def move_down(self):
        pos = int(self.file_list.curselection()[0])
        if pos != self.file_list.size()-1:
            fname = self.file_list.get(pos)
            self.file_list.delete(pos)
            self.file_list.insert(pos+1, fname)
            self.file_list.selection_set(pos+1)
            #falta mover el correspondiente en la lista interna

    

    def clear_list(self):
        """
            Limpiar Listado de archivos
        """
        self.file_list.delete(0, tk.END)
        self.files = []



if __name__ == "__main__":
    main = tk.Tk()
    app = MainFrame(main)
    main.mainloop()

