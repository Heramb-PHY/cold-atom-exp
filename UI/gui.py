import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import subprocess
import os
import time
import threading
from tkinter import filedialog, messagebox

class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master,attributes,**kw):
        super().__init__(master)
        self.attributes = attributes
        self.buttons = {}  # Dictionary to store button references

        for i,value in enumerate(self.attributes):
            button = customtkinter.CTkButton(self,text= value[0],command= value[1])
            button.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.buttons[value[0]] = button  # Store button reference by its text

class OutputBox(customtkinter.CTkTextbox):
    def __init__(self, master):
        super().__init__(master)
        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cold Atom Computer Control")
        self.geometry("824x688")
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.abort_flag = False  # Shared variable to control excecution loop

        basepath = os.path.dirname(__file__)
        self.excel_file_path = os.path.abspath(os.path.join(basepath, "..", "time_sequence.xlsx"))  #  saved Excel file path
        self.address_file_path = os.path.abspath(os.path.join(basepath, "..", "working_address.txt"))
        with open (self.address_file_path,"w") as f:
            f.write(self.excel_file_path)
        attributes_1 = [
                      ("Plot timeline",self.button_callback),
                      ("Generate Text File",lambda: threading.Thread(target=self.Generate_text_file).start()),
                      ("Execute", lambda: threading.Thread(target=self.execute).start()) ,
                      ("Execute 100 times",lambda: threading.Thread(target=self.execute_multi, args=(100,)).start()),
                      ("Execute Multiple",lambda: threading.Thread(target=self.execute_manual_multi).start()),]
        self.button_frame_1 = ButtonFrame(self,attributes=attributes_1)
        self.button_frame_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        self.entry = customtkinter.CTkEntry(self.button_frame_1, placeholder_text="Multiple Entry")
        self.entry.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="nsw")

        attributes_2 = [("Select Excel File",lambda: threading.Thread(target=self.open_excel_file).start()),
                        ("Default Excel File",lambda: threading.Thread(target=self.default_excel_file).start()),
                        ("Abort",self.abort)]
        self.button_frame_2 = ButtonFrame(self,attributes=attributes_2)
        self.OutputBox_filename = customtkinter.CTkLabel(self.button_frame_2,text="Default Excel file",font=("Cascadia Code",12))
        self.OutputBox_filename.grid(row=0,column=0,padx=10, pady=(10, 0), sticky="nsw")
        self.button_frame_2.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsw")

        self.OutputBox = OutputBox(self)
        self.OutputBox.configure(font=("Cascadia Code",12),wrap='word')
        #self.OutputBox.configure(state="disabled")
        self.OutputBox.grid(row=1, column=0,columnspan = 2,padx=10, pady=(10, 0), sticky="news")

        self.create_figure()

    def button_callback(self):
            print("Hello")

    def create_figure(self):
        px = 1/plt.rcParams['figure.dpi']
        self.figure = Figure(figsize=(443*px, 651*px))
        self.ax = self.figure.add_subplot(111)
        self.ax.plot([1, 2, 3, 4, 5], [2, 3, 5, 7, 11])
        self.ax.set_title("Sample Graph")
        self.ax.set_xlabel("Time")
        # Embed the figure in Tkinter
        canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=3, rowspan=2, padx=10, pady=(10, 0), sticky="nesw")

    def execute(self):
        button = self.button_frame_1.buttons["Execute"] # Block to get current color of button and change it to red.
        original_color = button.cget("fg_color")
        self.change_button_color(button, "red")

        basepath = os.path.dirname(__file__)
        executable_path = os.path.abspath(os.path.join(basepath, "..", "..","send_signal.exe"))
        executable_dir = os.path.dirname(executable_path)
        try:
             # Run the executable and capture the output
            result = subprocess.run([executable_path], cwd=executable_dir,capture_output=True, text=True)
            output = result.stdout
            
            # Display the output in the Text widget
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, output)
        except Exception as e:
            # Handle exceptions (e.g., file not found, permissions issues)
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, f"Error executing program: {e}")

        self.change_button_color(button, original_color) # Revert button color to original

    def Generate_text_file(self):

        button = self.button_frame_1.buttons["Generate Text File"] # Block to get current color of button and change it to red.
        original_color = button.cget("fg_color")
        self.change_button_color(button, "red")

        self.OutputBox.delete(1.0, customtkinter.END)
        basepath = os.path.dirname(__file__)
        executable_path = os.path.abspath(os.path.join(basepath, "..","main.py"))
        executable_dir = os.path.dirname(executable_path)
        try:
             # Run the executable and capture the output
            result = subprocess.run(["python",executable_path], cwd=executable_dir,capture_output=True, text=True)
            output = result.stdout
            error = result.stderr
            # Display the output in the Text widget
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, output)
            self.OutputBox.insert(customtkinter.END, error)
        except Exception as e:
            # Handle exceptions (e.g., file not found, permissions issues)
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, f"Error executing python timesequence program: {e}")

        self.change_button_color(button, original_color) # Revert button color to original

    def execute_multi(self, multiple_time):
        button = self.button_frame_1.buttons["Execute 100 times"] # Block to get current color of button and change it to red.
        original_color = button.cget("fg_color")
        self.change_button_color(button, "red")

        self.abort_flag = False  # Reset abort flag
        self.OutputBox.delete(1.0, customtkinter.END)
        self.OutputBox.insert(customtkinter.END, f"Executing {multiple_time} times.\n")
        basepath = os.path.dirname(__file__)
        executable_path = os.path.abspath(os.path.join(basepath, "..", "..","send_signal.exe"))
        executable_dir = os.path.dirname(executable_path)
        for i in range(0,multiple_time):
            if self.abort_flag:  # Check abort flag
                    self.OutputBox.insert(customtkinter.END, "\nExecution aborted.")
                    break
            try:
                # Run the executable and capture the output
                result = subprocess.run([executable_path], cwd=executable_dir,capture_output=True, text=True)
                output = result.stdout
                # Display the output in the Text widget
                if i == 0:
                    self.OutputBox.insert(customtkinter.END, output)
                #self.OutputBox.delete("end-1l","end")
                self.OutputBox.insert(customtkinter.END, "\n"+str(i+1))
                time.sleep(1)
                self.OutputBox.delete("end-1l","end")
            except Exception as e:
                # Handle exceptions (e.g., file not found, permissions issues)
                self.OutputBox.delete(1.0, customtkinter.END)
                self.OutputBox.insert(customtkinter.END, f"Error executing program: {e}")
        
        self.OutputBox.insert(customtkinter.END, f"\n Multiple {i+1} times completed.")
        self.change_button_color(button, original_color) # Revert button color to original

    def execute_manual_multi(self):
        text = self.entry.get()
        if text == "" :
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, f"You have entered nothing. Please enter numeric value in Muliplte Entry text box.")
        iteration = int(text)
        if iteration >= 30 :
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, f"Please enter the values less than or equal 30 in Muliplte Entry text box. ")
        else:
            self.execute_multi(iteration)

    def abort(self):
        self.abort_flag = True  # Set abort flag

    
    def change_button_color(self, button, color):
        button.configure(fg_color=color)

    def save_excel_file(self):
        pass

    def open_excel_file(self):
        file = customtkinter.filedialog.askopenfile(mode='r',filetypes=[("Excel files",'*.xlsx')])
        if file:
            self.excel_file_path = os.path.abspath(file.name)
            with open (self.address_file_path,"w") as f:
                    f.write(self.excel_file_path)
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, f"Excel file at location {self.excel_file_path} is selected. ")
            # Extract the file name and update the label
            file_name = os.path.basename(file.name)
            self.OutputBox_filename.configure(text=file_name)

    def default_excel_file(self):
        basepath = os.path.dirname(__file__)
        self.excel_file_path = os.path.abspath(os.path.join(basepath, "..", "time_sequence.xlsx"))  #  saved Excel file path
        self.address_file_path = os.path.abspath(os.path.join(basepath, "..", "working_address.txt"))
        with open (self.address_file_path,"w") as f:
            f.write(self.excel_file_path)
        self.OutputBox.delete(1.0, customtkinter.END)
        self.OutputBox.insert(customtkinter.END, f"Default Excel file {self.excel_file_path} is selected. ")
    
if __name__ == "__main__":
    app = App()
    app.mainloop()