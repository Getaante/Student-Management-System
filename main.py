from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

# Student management system 
class SMS:
  
    def __init__(self,root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry('430x385')
        self.root.resizable(0,0)
        self.root.configure(background="gray")
        # variables ..
        self.condition = True
        self.search = StringVar()
        self.name = StringVar()
        self.roll = IntVar()  # the default value of roll and age variable is 0 and it will also shown in entry box
        self.roll.set("")       # and to remove that 0 i use .set("") method ........
        self.course = StringVar()
        self.age = IntVar()
        self.age.set("")
        self.dob = StringVar()


        self.entry_frame = LabelFrame(self.root,text="Enter data here",fg='gold',bg="grey",font=('arial',10,'bold'),bd=5,relief=RIDGE)
        self.entry_frame.place(x=0,y=0,width=300,height=235)
        # adding entry boxes and labels in entry frame ...

        # labels .....
        self.name_label = Label(self.entry_frame,text="Name : ",font=('arial',10,'bold'),width=11)
        self.name_label.grid(row=0,column=0,ipadx=10,ipady=8)

        self.roll_label = Label(self.entry_frame, text="Roll no. : ", font=('arial', 10, 'bold'),width=11)
        self.roll_label.grid(row=1, column=0,ipadx=10,ipady=8)

        self.course_label = Label(self.entry_frame, text="Course : ", font=('arial', 10, 'bold'),width=11)
        self.course_label.grid(row=2, column=0,ipadx=10,ipady=8)

        self.age_label = Label(self.entry_frame, text="Age : ", font=('arial', 10, 'bold'),width=11)
        self.age_label.grid(row=3, column=0,ipadx=10,ipady=8)

        self.dob_label = Label(self.entry_frame, text="DOB : ", font=('arial', 10, 'bold'),width=11)
        self.dob_label.grid(row=4, column=0,ipadx=10,ipady=8)

        # Entry boxes to getting data ....
        self.name_entry = Entry(self.entry_frame,width=20,font=('arial',10,),bd=3,textvariable=self.name)
        self.name_entry.grid(row=0,column=1,ipadx=10,ipady=8)

        self.roll_entry = Entry(self.entry_frame, width=20, font=('arial', 10,), bd=3,textvariable=self.roll)
        self.roll_entry.grid(row=1, column=1, ipadx=10, ipady=8)

        self.course_entry = Entry(self.entry_frame, width=20, font=('arial', 10,), bd=3,textvariable=self.course)
        self.course_entry.grid(row=2, column=1, ipadx=10, ipady=8)

        self.age_entry = Entry(self.entry_frame, width=20, font=('arial', 10,), bd=3,textvariable=self.age)
        self.age_entry.grid(row=3, column=1, ipadx=10, ipady=8)

        self.dob_entry = Entry(self.entry_frame, width=20, font=('arial', 10,), bd=3,textvariable=self.dob)
        self.dob_entry.grid(row=4, column=1, ipadx=10, ipady=8)

        # button frame for adding buttons ...

        self.button_frame = LabelFrame(self.root,text="Controls ",fg='gold',bg="grey",font=('arial',10,'bold'),bd=5,relief=RIDGE)
        self.button_frame.place(x=300,y=0,width=130,height=235)

        self.save_button = Button(self.button_frame,text="Save", font=('arial', 10,"bold"), bd=3,width=4,command=self.save_data)
        self.save_button.grid(row=0,column=0,ipadx=10,padx=12,pady=4)

        self.update_button = Button(self.button_frame, text="Update", font=('arial', 10, "bold"), bd=3, width=4,command=self.update_data)
        self.update_button.grid(row=1, column=0, ipadx=10, padx=12, pady=4)

        self.delete_button = Button(self.button_frame, text="Delete", font=('arial', 10, "bold"), bd=3, width=4,command=self.delete_data)
        self.delete_button.grid(row=2, column=0, ipadx=10, padx=12, pady=4)

        self.clear_button = Button(self.button_frame, text="Clear", font=('arial', 10, "bold"), bd=3, width=4,command=self.clear_entry_boxes)
        self.clear_button.grid(row=3, column=0, ipadx=10, padx=12, pady=4)

        # entry box for search by number
        self.search_entry = Entry(self.button_frame,width=10,bd=3,textvariable=self.search)
        self.search_entry.grid(row=4,column=0,ipadx=5)

        # search button ..
        self.search_button = Button(self.button_frame, text="Search", font=('arial', 10, "bold"), bd=3, width=8,command=self.search_data)
        self.search_button.grid(row=5, column=0, ipadx=10, padx=12, pady=4)

        # set the scroll bar with tree view ....
        self.scroll_y = Scrollbar(self.root, orient=VERTICAL,bg="grey",bd=3)
        self.Student_table = ttk.Treeview(self.root,columns=("name", "roll", "course", "age", "dob"),yscrollcommand=self.scroll_y.set)
        self.scroll_y.place(x=410,y=235,height=150)
        self.scroll_y.config(command=self.Student_table.yview)
        # ==== content in Student Table==========
        self.Student_table.heading("name", text="Name")
        self.Student_table.heading("roll", text="Roll")
        self.Student_table.heading("course", text="Course")
        self.Student_table.heading("age", text="Age")
        self.Student_table.heading("dob", text="D.O.B")

        self.Student_table['show'] = 'headings'
        self.Student_table.column("name", width=20)
        self.Student_table.column("roll", width=5)
        self.Student_table.column("course", width=10)
        self.Student_table.column("age", width=5)
        self.Student_table.column("dob", width=10)

        self.Student_table.place(x=0,y=235,width=410,height=150)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

     # functions .....
    def save_data(self):
        if self.name.get()== "" or self.roll.get() == "" or self.course.get()=="" or self.age.get() == "" or self.dob.get() == "":
            messagebox.showerror("Please fill all entry feilds ")
        else:
            try:
                sqliteConnection = sqlite3.connect('student_database.db')
                cursor = sqliteConnection.cursor()

                sqlite_insert_query = """INSERT INTO record (name,roll,course,age,dob) VALUES (?,?,?,?,?);"""
                # Insert each entry values to a the spefic table. 
                data_tuple = (self.name.get(),self.roll.get(),self.course.get(),self.age.get(),self.dob.get())

                cursor.execute(sqlite_insert_query,data_tuple)
                sqliteConnection.commit()
                sqliteConnection.close()
                messagebox.showinfo("data is inserted")
                self.clear_entry_boxes()
                self.fetch_data()
            except sqlite3 as error:

                messagebox.showerror(" Error is "+str(error))

    def delete_data(self):
        try:
            sqliteConnection = sqlite3.connect('student_database.db')
            cursor = sqliteConnection.cursor()
            cursor.execute("DELETE FROM record WHERE roll = " + self.search.get())
            # for commit changes
            sqliteConnection.commit()
            # for closing data base connection
            cursor.close()
            messagebox.showinfo("data is deleted")
            x = self.Student_table.get_children()
            for item in x:
                self.Student_table.delete(item)
            self.fetch_data()
            self.clear_entry_boxes()
            self.search_button["text"] = " Search"

        except sqlite3.Error as e:
            messagebox.showerror("error\n please try again"+ str(e))

    def update_data(self):
        # enter roll number in search box for updation ....
        try:
            sqliteConnection = sqlite3.connect('student_database.db')
            cursor = sqliteConnection.cursor()
            sqlite_update_query = """ UPDATE record set name = ?,roll =? , course =?,age =?,dob =? where roll = ?"""
            data = (self.name.get(),self.roll.get(),self.course.get(),self.age.get(),self.dob.get(),self.roll.get())
            cursor.execute(sqlite_update_query,data)
            sqliteConnection.commit()
            cursor.close()
            messagebox.showinfo("Data is updated ")
            self.clear_entry_boxes()
            self.fetch_data()
            self.search_button["text"] = " Search"
        except sqlite3.Error as e:
            messagebox.showerror(" error occurs "+str(e))

    def search_data(self):
        if(self.condition):
            try:
                sqliteConnection = sqlite3.connect('student_database.db')
                cursor = sqliteConnection.cursor()
                sqlite_search_query = "SELECT * from record where roll = "+str(self.search.get())
                cursor.execute(sqlite_search_query)
                search_data = cursor.fetchone()
                sqliteConnection.commit()
                cursor.close()

                # inserting search data into table .
                if search_data != None:
                    self.Student_table.delete(*self.Student_table.get_children())
                    self.Student_table.insert('', END, values=search_data)
                     # changing the button text from search to show all
                    self.condition = False
                    self.search_button['text'] = "SHOW ALL"
                else:
                    messagebox.showerror("No such data of roll number "+ str(self.search.get()))
            except sqlite3.Error as e:
                messagebox.showerror(" AN error Occurs " + str(e))

        else:
            self.condition = True
            self.search_button["text"] = " Search"
            self.fetch_data()

    def clear_entry_boxes(self):
        self.name.set("")
        self.roll.set("")
        self.course.set("")
        self.age.set("")
        self.dob.set("")
        self.search.set("")

    def fetch_data(self):
        try:
            # connect to the db
            sqliteConnection = sqlite3.connect('student_database.db')

            cursor = sqliteConnection.cursor()
            # Select a specific query from a record 
            sqlite_select_query = """SELECT * from record"""
            cursor.execute(sqlite_select_query)
            data = cursor.fetchall()
            if len(data) != 0:
                self.Student_table.delete(*self.Student_table.get_children())
                for row in data:
                    self.Student_table.insert('', END, values=row)
                conn.commit()
                cursor.close()
        except:
            pass

    def get_cursor(self, event):
        cursor_row = self.Student_table.focus()
        contents = self.Student_table.item(cursor_row)
        row = contents['values']
        self.name.set(row[0])
        self.roll.set(row[1])
        self.course.set(row[2])
        self.age.set(row[3])
        self.dob.set(row[4])
        self.search.set(row[1])

if __name__=="__main__":
    root = Tk()
    SMS(root)
    root.mainloop()