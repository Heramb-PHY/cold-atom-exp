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

        attributes_1 = [
                      ("Plot timeline",self.button_callback),
                      ("Generate Text File",lambda: threading.Thread(target=self.Generate_text_file).start()),
                      ("Execute", lambda: threading.Thread(target=self.execute).start()) ,
                      ("Execute 100 times",lambda: threading.Thread(target=self.execute_multi, args=(100,)).start())]
        self.button_frame_1 = ButtonFrame(self,attributes=attributes_1)
        self.button_frame_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        attributes_2 = [("Select Excel File",self.button_callback),("Default Excel File",self.abort),("Abort",self.abort)]
        self.button_frame_2 = ButtonFrame(self,attributes=attributes_2)
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
        executable_path = os.path.abspath(os.path.join(basepath, "..", "..","send_signal_fake.exe"))
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
            
            # Display the output in the Text widget
            self.OutputBox.delete(1.0, customtkinter.END)
            self.OutputBox.insert(customtkinter.END, output)
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
        executable_path = os.path.abspath(os.path.join(basepath, "..", "..","send_signal_fake.exe"))
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

    def abort(self):
        self.abort_flag = True  # Set abort flag

    
    def change_button_color(self, button, color):
        button.configure(fg_color=color)

    def save_excel_file(self):
        pass
    
if __name__ == "__main__":
    app = App()
    app.mainloop()