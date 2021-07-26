from tkinter import *
import datetime


class GUI(Tk):
    def __init__(self):  # args sind hier die im GUI gebrauchten Validation-Funktionen
        Tk.__init__(self)
        self.val_funcs_dict = {}
        self.textbox_dict = {}
        self.textbox_list = []   # dafür da, dass man weiß in welcher Reihenfolge die entries erstellt wurden, damit man etwas mit dem objektnamen machen kann.
        self.label_dict = {}

    def register_val_funcs(self, *args):
        lambda_counter = 0
        for arg in args:
            if arg.__name__ == "<lambda>":
                func_name = "lambda" + str(lambda_counter)
                lambda_counter += 1
            else:
                func_name = arg.__name__
            self.val_funcs_dict.update({func_name: self.register(arg)})

    def draw_label(self, text, column, row, label_name=""):  # schnellere Möglichkeit ein Label einzufügen
        label = Label(self, text=text)
        label.grid(row=row, column=column, sticky="E")
        if label_name == "":
            label_name = text.split(" ")[0]
        self.label_dict.update({label_name: label})

    def draw_labels_textboxes(self, texts, column, row_start, textbox_width, attachment=""):  #
        textbox_funclist = []
        label_list = []
        row = row_start
        for text in texts:
            label = Label(self, text=text)
            textbox_funclist.append(Entry(self, width=textbox_width))
            label_list.append(label)
            label.grid(row=row, column=column, sticky="E")
            textbox_funclist[-1].grid(row=row, column=column + 1)
            row += 1
            self.textbox_list.append(text + attachment)
        self.textbox_dict.update({text + attachment: textbox for text, textbox in zip(texts, textbox_funclist)})

    def add_validation_to_textbox(self, textbox_name, func_name, validate_trigger, *args):  # args sind die args die tkinter der func senden sollen
        self.textbox_dict[textbox_name].config(validate=validate_trigger, validatecommand=(self.val_funcs_dict[func_name], args))
        print(args)


class ValidateFuncs:  # enthält alle möglichen validation funktionen, für tkinter geschrieben
    def __init__(self, gui_class):
        self.connected_class = gui_class

    def int_and_len(self, textbox_input, max_chars=0):  # wenn max nicht angegeben wird, checkt die Funktion nur nach int. braucht "%P". "key" macht sinn
        if textbox_input.isdigit():
            if max_chars:
                return self.length(textbox_input, max_chars)
            else:
                return True
        else:
            return False

    def length(self, string, max_chars):  # braucht "%P". "key" macht sinn
        return len(string) <= max_chars

    def date(self, textbox_input, textbox_name):  # braucht "%P". "key" macht sinn
        textbox_num = textbox_name[-1:]
        if textbox_num == "y":
            textbox_num = 0
        else:
            textbox_num -= 1
        if 8 <= len(textbox_input) <= 10:
            print(self.connected_class.textbox_dict[self.connected_class.textbox_list[int(textbox_num)]])
            date_list = textbox_input.split(".")
            try:
                datetime.date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
                self.connected_class.textbox_dict[self.connected_class.textbox_list[int(textbox_num)]].config(foreground="black")
            except ValueError and TypeError:
                self.connected_class.textbox_dict[self.connected_class.textbox_list[int(textbox_num)]].config(foreground="red")
            return True
        elif len(textbox_input) > 10:
            return False
        else:
            self.connected_class.textbox_dict[self.connected_class.textbox_list[int(textbox_num)]].config(foreground="black")
            return True


win = GUI()
funcs = ValidateFuncs(win)
win.register_val_funcs(lambda string: funcs.int_and_len(string, 6), lambda string: funcs.length(string, 15), funcs.date)
win.draw_label("Hallo", 1, 1)
win.draw_labels_textboxes(["kacke", "fwrghol", "koko"], 2, 1, 30)

# win.add_validation_to_textbox(win.textbox_dict["wiegehts"])
win.textbox_dict["fwrghol"].config(validate="key", validatecommand=(win.val_funcs_dict["date"], "%P", "%W"))
win.textbox_dict["kacke"].config(validate="key", validatecommand=(win.val_funcs_dict["date"], "%P", "%W"))

win.mainloop()