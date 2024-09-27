import os
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar

# Initialize the main application window
root = Tk()
root.title('Reservation System')
root.geometry('1350x786')


# Create a canvas for the background
can = Canvas(root, width=1350, height=786)
can.pack(fill='both', expand=True)

# Center the heading
can.create_text(675, 50, text='Train Reservation System', font=('Garamond', 40, 'bold italic'), fill='black')

# Connect to the SQLite database
conn = sqlite3.connect('train_booking.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS bookings (
             name TEXT, cnic TEXT PRIMARY KEY, email TEXT, cell TEXT, age TEXT, 
             destination_from TEXT, destination_to TEXT, train TEXT, time TEXT, price TEXT, date TEXT)''')

conn.commit()

# Function to open the selection window
def select():
    global variable, variable1, variable2, variable3, e6, rupee

    window1 = Toplevel(root)
    window1.title('Selection Process')
    window1.geometry('700x500')
    window1.config(bg='white')

    # Create selection dropdowns
    variable = StringVar(window1)
    variable.set('Dadar')
    drop = OptionMenu(window1, variable, 'Madgoan Junction', 'Ratnagiri', 'Sawantwadi', 'Dadar')
    drop.config(bg='white', fg='black', width=17, height=2)
    drop.place(x=160, y=20)
    fro = Label(window1, text='From', bg='yellow', fg='black', width=10)
    fro.place(x=30, y=20)

    variable1 = StringVar(window1)
    variable1.set('Madgoan Junction')
    drop1 = OptionMenu(window1, variable1, 'Ratnagiri', 'Sawantwadi', 'Madgoan Junction')
    drop1.config(bg='white', fg='black', width=17, height=2)
    drop1.place(x=520, y=20)
    to = Label(window1, text='To', bg='yellow', fg='black', width=10)
    to.place(x=420, y=20)

    variable2 = StringVar(window1)
    variable2.set('Vande Bharat')
    drop2 = OptionMenu(window1, variable2, 'Tejas Express', 'Madgoan Express', 'Kokan Kanya Express')
    drop2.config(bg='white', fg='black', width=17, height=2)
    drop2.place(x=520, y=220)

    variable3 = StringVar(window1)
    variable3.set('9am')
    drop3 = OptionMenu(window1, variable3, '9am', '10am', '12pm')
    drop3.config(bg='white', fg='black', width=17, height=2)
    drop3.place(x=520, y=120)
    timing_label = Label(window1, text='Timing', bg='yellow', fg='black', width=8)
    timing_label.place(x=420, y=130)

    # Function to calculate the price
    def calculate_price():
        global rupee
        destination_from = variable.get()
        destination_to = variable1.get()

        price_dict = {
            ('Madgoan Junction', 'Dadar'): 'Rs 2000',
            ('Madgoan Junction', 'Ratnagiri'): 'Rs 1000',
            ('Madgoan Junction', 'Sawantwadi'): 'Rs 1200',
            ('Dadar', 'Madgoan Junction'): 'Rs 3000',
            ('Dadar', 'Ratnagiri'): 'Rs 2000',
            ('Dadar', 'Sawantwadi'): 'Rs 1500',
            ('Ratnagiri', 'Dadar'): 'Rs 1800',
            ('Ratnagiri', 'Sawantwadi'): 'Rs 3000',
            ('Ratnagiri', 'Madgoan Junction'): 'Rs 1200',
            ('Sawantwadi', 'Dadar'): 'Rs 1200',
            ('Sawantwadi', 'Ratnagiri'): 'Rs 1500',
            ('Sawantwadi', 'Madgoan Junction'): 'Rs 1800'
        }

        rupee = price_dict.get((destination_from, destination_to), 'Price not available')

        price_label = Label(window1, text=rupee, bg='white', fg='black', width=17, height=2)
        price_label.place(x=160, y=100)

        next_button = Button(window1, text='Next', fg='black', bg='green', height=2, width=15, command=booking)
        next_button.place(x=520, y=310)

    price_button = Button(window1, text='Get Price', bg='white', fg='black', width=10, command=calculate_price)
    price_button.place(x=30, y=100)

    l6 = Label(window1, text='Select Date', fg='white', bg='purple', height=2, width=17)
    l6.place(x=30, y=200)
    e6 = Calendar(window1)
    e6.place(x=30, y=250)

# Function for booking
def booking():
    window = Toplevel(root)
    window.geometry('700x500')
    window.title('Booking')
    window.config(bg='white')

    if variable.get() == variable1.get():
        messagebox.showerror('Error', "Departure city and arrival city cannot be the same")
        return

    Label(window, text='Enter Name', fg='white', bg='purple', height=2, width=17).place(x=20, y=10)
    e1 = Entry(window, width=30)
    e1.place(x=220, y=20)

    Label(window, text='Enter CNIC', fg='white', bg='purple', height=2, width=17).place(x=20, y=70)
    e2 = Entry(window, width=30)
    e2.place(x=220, y=80)

    Label(window, text='Enter Email', fg='white', bg='purple', height=2, width=17).place(x=20, y=130)
    e3 = Entry(window, width=30)
    e3.place(x=220, y=140)

    Label(window, text='Enter Cell no', fg='white', bg='purple', height=2, width=17).place(x=20, y=190)
    e4 = Entry(window, width=30)
    e4.place(x=220, y=200)

    Label(window, text='Enter Age', fg='white', bg='purple', height=2, width=17).place(x=20, y=250)
    e5 = Entry(window, width=30)
    e5.place(x=220, y=260)

    def state():
        if e1.get() and e2.get() and e3.get() and e4.get() and e5.get():
            save_booking(e1.get(), e2.get(), e3.get(), e4.get(), e5.get())

    book = Button(window, text='Book a Ticket', height=2, width=15, bg='green', fg='black', command=state)
    book.place(x=220, y=320)

# Function to save booking to the database
def save_booking(name, cnic, email, cell, age):
    try:
        c.execute("INSERT INTO bookings (name, cnic, email, cell, age, destination_from, destination_to, train, time, price, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, cnic, email, cell, age, variable.get(), variable1.get(), variable2.get(), variable3.get(), rupee, e6.get_date()))
        conn.commit()
        done(name, cnic, email, cell, age)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "CNIC already exists. Please try updating the record.")

# Function to display booking details
def done(name, cnic, email, cell, age):
    booking_details = Toplevel(root)
    booking_details.title("Booking Details")
    booking_details.geometry("400x400")
    booking_details.config(bg='darkgrey')

    Label(booking_details, text="Booking Successful",bg='darkgrey' ,font=('Arial', 16, 'bold')).pack(pady=10)

    details = f"Name: {name}\nCNIC: {cnic}\nEmail: {email}\nCell: {cell}\nAge: {age}\nFrom: {variable.get()}\nTo: {variable1.get()}\nTrain: {variable2.get()}\nTime: {variable3.get()}\nDate: {e6.get_date()}\nPrice: {rupee}"

    Label(booking_details, text=details, bg='darkgrey', justify=LEFT).pack(pady=10)

# Function to update an existing booking
def update_booking():
    def find_booking():
        cnic = e_cnic.get()
        c.execute("SELECT * FROM bookings WHERE cnic=?", (cnic,))
        record = c.fetchone()
        if record:
            e_name.delete(0, END)
            e_email.delete(0, END)
            e_cell.delete(0, END)
            e_age.delete(0, END)
            e_name.insert(0, record[0])
            e_email.insert(0, record[2])
            e_cell.insert(0, record[3])
            e_age.insert(0, record[4])
        else:
            messagebox.showerror("Error", "Booking not found")

    def update_record():
        cnic = e_cnic.get()
        name = e_name.get()
        email = e_email.get()
        cell = e_cell.get()
        age = e_age.get()
        c.execute("UPDATE bookings SET name=?, email=?, cell=?, age=? WHERE cnic=?", (name, email, cell, age, cnic))
        conn.commit()
        messagebox.showinfo("Success", "Booking Updated")

    window = Toplevel(root)
    window.title("Update Booking")
    window.geometry("400x400")

    Label(window, text="Enter CNIC to Search", fg="black").pack(pady=10)
    e_cnic = Entry(window, width=30)
    e_cnic.pack(pady=5)

    search_button = Button(window, text="Find Booking", command=find_booking)
    search_button.pack(pady=10)

    Label(window, text="Name").pack(pady=5)
    e_name = Entry(window, width=30)
    e_name.pack(pady=5)

    Label(window, text="Email").pack(pady=5)
    e_email = Entry(window, width=30)
    e_email.pack(pady=5)

    Label(window, text="Cell No").pack(pady=5)
    e_cell = Entry(window, width=30)
    e_cell.pack(pady=5)

    Label(window, text="Age").pack(pady=5)
    e_age = Entry(window, width=30)
    e_age.pack(pady=5)

    update_button = Button(window, text="Update Booking", command=update_record)
    update_button.pack(pady=20)

# Function to delete a booking
def delete_booking():
    def remove_booking():
        cnic = e_cnic.get()
        c.execute("DELETE FROM bookings WHERE cnic=?", (cnic,))
        conn.commit()
        messagebox.showinfo("Success", "Booking Deleted")

    window = Toplevel(root)
    window.title("Delete Booking")
    window.geometry("300x200")

    Label(window, text="Enter CNIC to Delete", fg="black").pack(pady=10)
    e_cnic = Entry(window, width=30)
    e_cnic.pack(pady=5)

    delete_button = Button(window, text="Delete Booking", command=remove_booking)
    delete_button.pack(pady=10)

# Align the buttons on the reservation page in one line and center the heading
Button(root, text="Selection Process", bg='lightblue', fg='black', width=20, height=2, command=select).place(x=300, y=200)
Button(root, text="Update Ticket", bg='yellow', fg='black', width=20, height=2, command=update_booking).place(x=560, y=200)
Button(root, text="Delete Ticket", bg='red', fg='white', width=20, height=2, command=delete_booking).place(x=820, y=200)

root.mainloop()