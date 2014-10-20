#!/usr/bin/env python
# -*- coding: utf-8 -*-


import Tkinter as tk
import ttk
from tkFileDialog import askopenfilenames, asksaveasfilename
import tkMessageBox
import os
import random
from merge import MergeProcess



class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        self.files = []

        btn_select_files = tk.Button(self, text="Agregar Archivos", command=self.add_files, pady=10)
        btn_select_files.grid(row=0, column=1, pady=5)

        self.file_list = tk.Listbox(self, width=30)
        self.file_list.grid(row=1, column=0, rowspan=4, columnspan=2, padx=5)

        btn_up = tk.Button(self, text="Subir", command=self.move_up, width=8, pady=10)
        btn_up.grid(row=1, column=2, padx=5)
         
        btn_down = tk.Button(self, text="Bajar", command=self.move_down, width=8, pady=10)
        btn_down.grid(row=2, column=2)
        
        btn_delete = tk.Button(self, text="Quitar", command=self.delete_item, width=8, pady=10)
        btn_delete.grid(row=3, column=2)
        
        btn_clear = tk.Button(self, text="Limpiar", command=self.clear_list, width=8, pady=10)
        btn_clear.grid(row=4, column=2)

        btn_merge = tk.Button(self, text="Unir Archivos", command=self.merge_files, pady=10)
        btn_merge.grid(row=5, column=1, pady=5)


    def add_files(self):
        """
            Agregar Archivos
        """
        files = askopenfilenames(multiple=True)
        if os.name == 'nt':
            #es windows por alguna razon no convierte el string en una tupla
            #por lo que hay que hacerlo a mano una referencia del problema
            # http://bugs.python.org/issue5712
            files = self.master.tk.splitlist(files)
        for _file in files:
            fname = _file.split('/')[-1]

            row = [fname, _file]
            if 1:#row in self.files: #no se permiten archivos duplicados
                self.files.append(row)
                self.file_list.insert(tk.END, fname)


    def delete_item(self):
        """
            Quita el item seleccionado
        """
        try:
            pos = int(self.file_list.curselection()[0])
            self.files.pop(pos)
            #fname = self.file_list.get(pos)
            self.file_list.delete(pos, pos)

            print pos,fname
        except:
            pass


    def move_up(self):
        """
            Sube una posicion el item seleccionado
        """
        pos = int(self.file_list.curselection()[0])
        if pos != 0:
            fname = self.file_list.get(pos)
            self.file_list.delete(pos)
            self.file_list.insert(pos-1, fname)
            self.file_list.selection_set(pos-1)
            aux = self.files[pos]
            self.files[pos] = self.files[pos-1]
            self.files[pos-1] = aux


    def move_down(self):
        """
            Deciende una posicion el item seleccionado
        """
        pos = int(self.file_list.curselection()[0])
        if pos != self.file_list.size()-1:
            fname = self.file_list.get(pos)
            self.file_list.delete(pos)
            self.file_list.insert(pos+1, fname)
            self.file_list.selection_set(pos+1)
            aux = self.files[pos]
            self.files[pos] = self.files[pos+1]
            self.files[pos+1] = aux


    def clear_list(self):
        """
            Limpiar Listado de archivos
        """
        self.file_list.delete(0, tk.END)
        self.files = []


    def merge_files(self):
        """
            Seleccionar destion y llamar al processo de union de  archivos
        """
        if 1:#len(self.files) > 0:
            _output = asksaveasfilename()
            if _output == "":
                _output = "salida.txt"
            main = tk.Toplevel(self.master)
            _files = []
            for _file in self.files:
                _files.append(_file[1])
            _output = open(_output, 'w')
            progress = MergeProgress(root=main, files=_files, output=_output)



class MergeProgress(tk.Frame):
    """
        Ventana de Progreso de copiado
    """
    def __init__(self, root, files=[], output='salida.txt'):
        tk.Frame.__init__(self, master=root)
        self.files = files
        self.output = output
        self.size = len(self.files)
        self.pack()

        lbl = tk.Label(self, text="Uniendo Archivos..")
        lbl.grid(row=0, pady=10, padx=10, sticky=tk.W)

        self.gauge = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, maximum=self.size)
        self.gauge.grid(row=1, padx=10)

        separator = ttk.Separator(self)
        separator.grid(row=2, pady=10)

        #iniciar union 
        self.merge = MergeProcess(self.files, self.output, self.gauge)
        self.merge.start()
        self.get_merge_status()


    def get_merge_status(self):
        """
            Unir
        """
        if self.merge.is_run:
            self.master.after(100, self.get_merge_status)

        else:
            self.gauge.stop()
            self.output.close()
            tkMessageBox.showinfo('Informacion', 'Finalizo el Copiado')
            self.master.destroy()



if __name__ == "__main__":
    main = tk.Tk()
    main.title('Text Merge')
    app = MainFrame(main)
    main.mainloop()

