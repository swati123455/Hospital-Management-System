import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk
from random import randint
from tkcalendar import Calendar
import mysql.connector
import hashlib

connection = mysql.connector.connect(host='localhost',
                                     database='CMS',
                                     user='root',
                                     password='')
cursor = connection.cursor()

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Management System")
        self.root.geometry("700x500")
        self.root.configure(bg="#3d587a")

        label_heading = tk.Label(root, text="Clinic Management System", font=("Helvetica", 28, "bold"), bg="#3d587a")
        label_heading.pack(pady=20)

        frame_elements = tk.Frame(root, bg="#c4ddf5", bd=2, relief=tk.RAISED)
        frame_elements.pack(pady=40)

        self.label_username = tk.Label(frame_elements, text="Username:", font=("Helvetica", 20, "bold"), bg="#c4ddf5", fg="#3d587a")
        self.label_username.grid(row=0, column=0, padx=10, pady=20, sticky=tk.E)
        self.entry_username = tk.Entry(frame_elements, font=("Helvetica", 20, "bold"), bg="#c4ddf5", fg="#3d587a", highlightbackground="#3d587a")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.label_password = tk.Label(frame_elements, text="Password:", font=("Helvetica", 20, "bold"), bg="#c4ddf5", fg="#3d587a")
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_password = tk.Entry(frame_elements, font=("Helvetica", 20, "bold"), bg="#c4ddf5", fg="#3d587a", highlightbackground="#3d587a",show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        button_login = tk.Button(frame_elements, text="Login", command=self.login, bg="#c4ddf5", fg="#3d587a", font=("Helvetica", 18, "bold"), highlightbackground="#3d587a")
        button_login.grid(row=2, column=0, columnspan=2, pady=15)

        button_forgot_password = tk.Button(frame_elements, text="Forgot Password", command=self.forgot_password, bg="#c4ddf5", fg="#3d587a", font=("Helvetica", 18, "bold"), highlightbackground="#3d587a")
        button_forgot_password.grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "1234":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.root.destroy()  # Close login window
            home_page = HomePage()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def forgot_password(self):

        security_question = "What is your dog's name?"
        correct_answer = "bruno"

        user_answer = simpledialog.askstring("Security Question", security_question)

        if user_answer and user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("Reset Password", "Your answer is correct! Your password is 1234")
        else:
            messagebox.showerror("Reset Password", "The answer provided is incorrect.")


class HomePage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clinic Management System - Home Page")
        self.root.geometry("1500x800")
        self.root.configure(bg="#3d587a")

        label_new = tk.Label(self.root, text="Clinic Management System", font=("Helvetica", 28, "bold"), bg="#3d587a")
        label_new.grid(row=0, column=0, pady=40, columnspan=4)

        buttons_frame = tk.Frame(self.root, bg="#3d587a")
        buttons_frame.grid(row=1, column=0)

        button_home = tk.Button(buttons_frame, text="Home", command=self.go_to_home, bg="#3d587a", fg="#3d587a", font=("Helvetica", 18, "bold"), highlightbackground="#3d587a", width=20, height=2)
        button_home.grid(row=0, column=0)

        button_patient = tk.Button(buttons_frame, text="Patient", command=self.open_patient_window, bg="#3d587a", fg="#3d587a", font=("Helvetica", 18, "bold"), highlightbackground="#3d587a", width=20, height=2)
        button_patient.grid(row=0, column=1)

        button_prescription = tk.Button(buttons_frame, text="Prescription", command=self.open_prescription_window, bg="#3d587a", fg="#3d587a", font=("Helvetica", 18, "bold"), highlightbackground="#3d587a", width=20, height=2)
        button_prescription.grid(row=0, column=2)

        button_logout = tk.Button(buttons_frame, text="Logout", command=self.logout, bg="#3d587a", fg="#3d587a", font=("Helvetica", 18, "bold"), highlightbackground="#3d587a", width=20, height=2)
        button_logout.grid(row=0, column=3)

        search_frame = tk.Frame(self.root, bg='#3d587a')
        search_frame.grid(row=1, column=1, pady=(20, 10), padx=20, sticky='w')

        self.search_entry = tk.Entry(search_frame, font=("Arial", 20), bg="#c4ddf5", fg="#3d587a")
        self.search_entry.pack(side='left', padx=(10, 5), fill='x', expand=True)

        search_button = tk.Button(search_frame, text='Search', command=self.fetch_patient_details, bg="#3d587a", fg="#3d587a", font=("Helvetica", 16, "bold"), highlightbackground="#3d587a", width=5, height=1)
        search_button.pack(side='left', padx=(5, 10))

        self.info_text = tk.Text(self.root, height=20, width=100, bg='#c4ddf5',fg="#3d587a", font=("Helvetica", 18, "bold"))
        self.info_text.grid(row=2, column=0, columnspan=2, padx=20, pady=100)

        self.root.mainloop()

    def go_to_home(self):
        messagebox.showinfo("Navigation", "You are already on the Home page.")

    def open_patient_window(self):
        popup_window = tk.Toplevel(self.root)
        patient_window = PatientWindow(popup_window)

    def open_prescription_window(self):
        popup_window = tk.Toplevel(self.root)
        prescription_window = PrescriptionWindow(popup_window)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        login_page = LoginPage(root)
        root.mainloop()

    def search_patient(self):
        search_query = self.search_entry.get()
        self.info_text.insert('end', f"Search for patient: {search_query}\n")


    def fetch_patient_details(self):
        patient_id = self.search_entry.get()

        try:

            query = "SELECT * FROM PatientRegistration WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            patient_details = cursor.fetchone()

            if patient_details:
                self.info_text.delete('1.0', 'end')
                headings = ["Patient ID:\t", "First Name:\t",  "Last Name:\t", "Address:\t", "Phone:\t", "Gender:\t", "DOB:\t"]
                for index, heading in enumerate(headings):
                    detail = patient_details[index]  # Get patient detail based on index
                    self.info_text.insert('end', f"{heading} {detail}\n")

            else:
                messagebox.showerror("Error", "Patient ID not found")

        except mysql.connector.Error as error:
            print(f"Failed to fetch patients details: {error}")
        finally:
            if 'connection' in locals():
                if connection.is_connected():
                    cursor.close()
                    connection.close()

class PatientWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("New Patient Window")
        self.root.geometry("1500x800")
        self.root.configure(bg="#3d587a")

        label_patient = tk.Label(root, text="Patient Registration", font=("Helvetica", 28, "bold"), bg="#3d587a")
        label_patient.grid(row=0, column=1, pady=10, columnspan=1, sticky='w')

        self.patient_id = randint(1000, 9999)
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.address = StringVar()
        self.phone_number = StringVar()
        self.gender = StringVar()
        self.date_of_birth = StringVar()

        label_patient_id = Label(root, text="Patient ID:", font=("Helvetica", 16), bg="#3d587a")
        label_patient_id.grid(row=1, column=0, sticky='e',pady = 15, padx = 20)

        entry_patient_id = Entry(root, font=("Helvetica", 16), bg="#c4ddf5", fg="#3d587a")
        entry_patient_id.insert(0, self.patient_id)
        entry_patient_id.grid(row=1, column=1, sticky='w', pady=15)

        label_first_name = Label(root, text="First Name:", font=("Helvetica", 16), bg="#3d587a")
        label_first_name.grid(row=2, column=0, sticky='e',pady = 15, padx = 20)

        entry_first_name = Entry(root, textvariable=self.first_name, font=("Helvetica", 16),bg="#c4ddf5", fg="#3d587a")
        entry_first_name.grid(row=2, column=1, sticky='w')

        label_last_name = Label(root, text="Last Name:", font=("Helvetica", 16), bg="#3d587a")
        label_last_name.grid(row=3, column=0, sticky='e',pady = 15, padx = 20)

        entry_last_name = Entry(root, textvariable=self.last_name, font=("Helvetica", 16),bg="#c4ddf5", fg="#3d587a")
        entry_last_name.grid(row=3, column=1, sticky='w')

        label_address = Label(root, text="Address:", font=("Helvetica", 16), bg="#3d587a")
        label_address.grid(row=4, column=0, sticky='e',pady = 15, padx = 20)

        entry_address = Entry(root, textvariable=self.address, font=("Helvetica", 16),bg="#c4ddf5", fg="#3d587a")
        entry_address.grid(row=4, column=1, sticky='w')

        label_phone_number = Label(root, text="Phone Number:", font=("Helvetica", 16), bg="#3d587a")
        label_phone_number.grid(row=5, column=0, sticky='e',pady = 15, padx = 20)

        entry_phone_number = Entry(root, textvariable=self.phone_number, font=("Helvetica", 16),bg="#c4ddf5", fg="#3d587a")
        entry_phone_number.grid(row=5, column=1, sticky='w')

        label_gender = Label(root, text="Gender:", font=("Helvetica", 14), bg="#3d587a")
        label_gender.grid(row=6, column=0, sticky='e',pady = 15, padx = 20)

        style = ttk.Style()
        style.theme_use('clam')
        gender_options = ["Male", "Female", "Other"]
        dropdown_gender = ttk.Combobox(root, values=gender_options, textvariable=self.gender, font=("Helvetica", 16))
        style.configure('TCombobox', fieldbackground='#c4ddf5', background="#3d587a")
        dropdown_gender.grid(row=6, column=1, sticky='w')

        label_dob = Label(root, text="Date of Birth:", font=("Helvetica", 16), bg="#3d587a")
        label_dob.grid(row=7, column=0, sticky='e',pady = 15, padx = 20)

        entry_dob = Entry(root, textvariable=self.date_of_birth, font=("Helvetica", 16),bg="#c4ddf5", fg="#3d587a")
        entry_dob.grid(row=7, column=1, sticky='w')

        button_save = Button(root, text="Save", command=self.save_patient_details, bg="#c4ddf5", fg="#3d587a",font=("Helvetica", 18),width=15, height=1)
        button_save.grid(row=8,column=0, sticky='e',pady = 15, padx = 20)

        exit = Button(root, text="Back", command=self.root.destroy, bg="#c4ddf5", fg="#3d587a",font=("Helvetica", 18),width=15, height=1)
        exit.grid(row=8, column=1, sticky='w', pady=15)

        self.patient_table = ttk.Treeview(root, columns=(
        "Patient ID", "First Name", "Last Name", "Address", "Phone Number", "Gender", "Date of Birth"))
        self.patient_table.heading("#0", text="Patient Details")
        self.patient_table.heading("Patient ID", text="Patient ID")
        self.patient_table.heading("First Name", text="First Name")
        self.patient_table.heading("Last Name", text="Last Name")
        self.patient_table.heading("Address", text="Address")
        self.patient_table.heading("Phone Number", text="Phone Number")
        self.patient_table.heading("Gender", text="Gender")
        self.patient_table.heading("Date of Birth", text="Date of Birth")
        self.patient_table.grid(row=9, column=0, columnspan=2)

        self.adjust_column_widths()

    def adjust_column_widths(self):
        screen_width = self.root.winfo_screenwidth()
        for idx, column in enumerate(self.patient_table['columns']):
            col_width = screen_width // len(self.patient_table['columns']) - 20
            self.patient_table.column(column, width=col_width)

    def save_patient_details(self):
        global cursor, connection
        patient_data = [
            self.patient_id,
            self.first_name.get(),
            self.last_name.get(),
            self.address.get(),
            self.phone_number.get(),
            self.gender.get(),
            self.date_of_birth.get()
        ]
        self.patient_table.insert("", "end", text="Patient " + str(self.patient_id), values=patient_data)

        try:


            insert_query = "INSERT INTO PatientRegistration (patient_id, first_name, last_name, address, phone_number, gender, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, patient_data)
            connection.commit()

            messagebox.showinfo("Success", "Patient details saved successfully!")

        except mysql.connector.Error as error:
            print(f"Failed to insert record into patients table: {error}")

        finally:
            if 'connection' in locals():
                if connection.is_connected():
                    cursor.close()
                    connection.close()

class PrescriptionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Prescription")
        self.root.geometry("1500x800")
        self.root.configure(bg="#3d587a")

        label_patient = tk.Label(root, text="Patient Prescription", font=("Helvetica", 28, "bold"), bg="#3d587a")
        label_patient.grid(row=0, column=0, pady=10, columnspan=2)

        patient_ids = self.fetch_patient_ids()

        self.prescription_id = 1
        self.medication = StringVar()
        self.dosage = StringVar()
        self.frequency = StringVar()
        self.duration = StringVar()

        label_patient_id = Label(root, text="Patient ID:", font=("Helvetica", 16), bg="#3d587a")
        label_patient_id.grid(row=1, column=0, sticky='e', pady=15, padx=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TMenubutton', background='#c4ddf5', foreground='#3d587a')

        self.patient_id_var = StringVar()
        self.patient_id_var.set(patient_ids[0] if patient_ids else "")

        patient_id_dropdown = OptionMenu(root, self.patient_id_var, *patient_ids)
        patient_id_dropdown.grid(row=1, column=1, sticky='w', pady=15)

        style.configure(menu=patient_id_dropdown["menu"], style='Custom.TMenubutton')

        label_medication = Label(root, text="Medication:", font=("Helvetica", 16), bg="#3d587a")
        label_medication.grid(row=3, column=0, sticky='e', pady=15, padx=10)

        entry_medication = Entry(root, textvariable=self.medication, font=("Helvetica", 16), bg="#c4ddf5", fg="#3d587a")
        entry_medication.grid(row=3, column=1, sticky='w')

        label_dosage = Label(root, text="Dosage:", font=("Helvetica", 16), bg="#3d587a")
        label_dosage.grid(row=4, column=0, sticky='e', pady=15, padx=10)

        entry_dosage = Entry(root, textvariable=self.dosage, font=("Helvetica", 16), bg="#c4ddf5", fg="#3d587a")
        entry_dosage.grid(row=4, column=1, sticky='w')

        label_frequency = Label(root, text="Frequency:", font=("Helvetica", 16), bg="#3d587a")
        label_frequency.grid(row=5, column=0, sticky='e', pady=15, padx=10)

        entry_frequency = Entry(root, textvariable=self.frequency, font=("Helvetica", 16), bg="#c4ddf5", fg="#3d587a")
        entry_frequency.grid(row=5, column=1, sticky='w')

        label_duration = Label(root, text="Duration:", font=("Helvetica", 16), bg="#3d587a")
        label_duration.grid(row=6, column=0, sticky='e', pady=15, padx=10)

        entry_duration = Entry(root, textvariable=self.duration, font=("Helvetica", 16), bg="#c4ddf5", fg="#3d587a")
        entry_duration.grid(row=6, column=1, sticky='w')

        button_save = Button(root, text="Save", command=self.save_prescription_details, bg="#c4ddf5", fg="#3d587a", font=("Helvetica", 18), width=15, height=1)
        button_save.grid(row=7, column=0, sticky='e',pady = 15, padx = 20)

        exit_button = Button(root, text="Back", command=self.root.destroy, bg="#c4ddf5", fg="#3d587a", font=("Helvetica", 18), width=15, height=1)
        exit_button.grid(row=7, column=1, sticky='w', pady=15)

        print_button = Button(root, text="Export", command=self.print_prescription_table, bg="#c4ddf5", fg="#3d587a", font=("Helvetica", 18), width=15, height=1)
        print_button.grid(row=7, column=1, sticky='w', pady=15,padx = 220)

        self.prescription_table = ttk.Treeview(root, columns=("Patient ID", "Prescription ID", "Medication", "Dosage", "Frequency", "Duration"))
        self.prescription_table.heading("#0", text="Patient ID")
        self.prescription_table.heading("Patient ID", text="Patient ID")
        self.prescription_table.heading("Prescription ID", text="Prescription ID")
        self.prescription_table.heading("Medication", text="Medication")
        self.prescription_table.heading("Dosage", text="Dosage")
        self.prescription_table.heading("Frequency", text="Frequency")
        self.prescription_table.heading("Duration", text="Duration")
        self.prescription_table.grid(row=9, column=0, columnspan=2)

        self.adjust_column_widths()

    def adjust_column_widths(self):
        screen_width = self.root.winfo_screenwidth()
        for idx, column in enumerate(self.prescription_table['columns']):
            col_width = screen_width // len(self.prescription_table['columns']) - 20
            self.prescription_table.column(column, width=col_width)

    def save_prescription_details(self):
        global connection, cursor
        prescription_data = [
            self.patient_id_var.get(),
            self.prescription_id,
            self.medication.get(),
            self.dosage.get(),
            self.frequency.get(),
            self.duration.get()
        ]
        self.prescription_table.insert("", "end", text="Patient " + str(self.patient_id_var.get()), values=prescription_data)

        self.prescription_id += 1
        if self.prescription_id > 100:
            self.prescription_id = 1

        self.medication.set("")
        self.dosage.set("")
        self.frequency.set("")
        self.duration.set("")

        try:
            insert_query = "INSERT INTO Prescription (prescription_id, patient_id, medication, dosage, frequency, duration) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, prescription_data)
            connection.commit()

            messagebox.showinfo("Success", "Prescription saved successfully!")
        except mysql.connector.Error as error:
            print(f"Failed to insert record into patients table: {error}")
        finally:
            if 'connection' in locals():
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def print_prescription_table(self):
        filename = "prescription_table.txt"
        with open(filename, "w") as file:
            for item in self.prescription_table.get_children():
                values = self.prescription_table.item(item, "values")
                line = "\t".join(str(value) for value in values) + "\n"
                file.write(line)
        messagebox.showinfo("Print", "Prescription details exported to prescription_table.txt")

    def fetch_patient_ids(self):
        patient_ids = []

        try:

            query = "SELECT patient_id FROM PatientRegistration"
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                patient_ids.append(row[0])


        except mysql.connector.Error as error:
            print(f"Error fetching patient IDs: {error}")

        finally:
            if 'connection' in locals():
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        return patient_ids

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()