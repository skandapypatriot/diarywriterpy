import sqlite3
from datetime import datetime
from time import strftime
from tkinter import *
from tkinter import messagebox, scrolledtext
from tkinter import filedialog

root = Tk()
conn = sqlite3.connect("dairy.db")
c = conn.cursor()

# defintions

## fetcher function --> It fetches the the data from the scrolledtext widget and inserts it into the database 
def fechter():
    
    tl = Toplevel(root, )
   
    
    ### This function changes the number of days by get the month (To detrmine the if it's 30 or 31 days) and year(To caluculate tif its a leap year)  
    def day_change():
        
        if month % 2 == 0 and not month == 2:
            day_sb.config(from_=1 , to=30)
            
        elif month % 2 == 1 and not month == 2:
            day_sb.config(from_=1 , to=31)
            
        elif month == 2 and int(year_sb.get()) % 4 == 0:
            day_sb.config(from_=1 , to=29)
            
        elif month == 2 and not int(year_sb.get()) % 4 == 0:
            day_sb.config(from_=1 , to=28)

    ### This interacts with the database to get data
    def fectch():
        
        global date
        
        date = f'{int(day_sb.get()):02}/{int(month_sb.get()):02}/{int(year_sb.get()):02}'
        
        data = tuple(c.execute(f'''select content from diary where datetime='{date}' '''))
        
        if not data == ():
            sc.config(state=NORMAL)
            
            sc.delete(1.0, END)
            sc.insert(1.0, data[0][0])
            
            tl.destroy()
        else:
            messagebox.showinfo("Diary", "Sorry but the date spcified is't found in the database or it not written yet ")
        
    day_sb = Spinbox(tl, from_=1, to=31)
    month_sb = Spinbox(tl, from_=1, to=12, command=day_change)
    year_sb = Spinbox(tl, from_=2000 ,to=3000)
    enter_button = Button(tl,  text="Enter", command=fectch)
    date = ""
    
    day_sb.pack()
    month_sb.pack()
    year_sb.pack()
    enter_button.pack()
    
    tl.mainloop()

## insert_data --> Inserts the data into the database. If the data is already entered then show an error
def insert_data():
    
    if not entered:
        content = sc.get(1.0, END)
        sc.delete(1.0, END)
        
        c.execute(f"INSERT INTO diary VALUES ('{datetime_create()[1]}', '{content}')")
        conn.commit()
        
        sc.config(state=DISABLED)
        
    if entered:
        messagebox.showinfo("Diary" , f"Sorry, but you have already enter the diary for {datetime_create()[1]}")
        tl.destroy()
## date_create --> Gives a starting text and date 
def datetime_create():
    
    day = strftime("%c")[:3]
    date = ""
    date_raw = str(datetime.now())[:10]
    year, month, day_num = date_raw.split("-")
    
    date = day_num + "/" + month + "/" + year
    
    time_raw = strftime("%H:%M")
    hour, mins = time_raw.split(":")
    hour, mins = int(hour), int(mins)
    
    f = "AM"
    if hour > 12:
        hour = hour - 12
        f = "PM"
        
    time = f"{hour}:{mins}{f}"

    s_t = day + "\n" + date + " ~ " + time + "\n" + "Dear dairy, " + "\n"
    
    return [s_t, date, ]
    
## format_data_base --> Formats the entire database 
def format_data_base():
    c.execute("DELETE from diary")
    conn.commit()
    entered = False


def download_db():
    tl2 = Toplevel(root, )

    ### This function changes the number of days by get the month (To detrmine the if it's 30 or 31 days) and year(To caluculate tif its a leap year)  
    def day_change():
        month = int(month_sb.get())
        if month % 2 == 0 and not month == 2:
            day_sb.config(from_=1 , to=30)
            
        elif month % 2 == 1 and not month == 2:
            day_sb.config(from_=1 , to=31)
            
        elif month == 2 and int(year_sb.get()) % 4 == 0:
            day_sb.config(from_=1 , to=29)
            
        elif month == 2 and not int(year_sb.get()) % 4 == 0:
            day_sb.config(from_=1 , to=28)
    
    def download():
        date = f'{int(day_sb.get()):02}/{int(month_sb.get()):02}/{int(year_sb.get()):02}'
        dir = filedialog.askdirectory() 
        data = tuple(c.execute(f'''select * from diary where datetime='{date}' '''))
        
        if not data == ():
            title = data[0][0]
            content = data[0][1]
            day_num, month, year = title.split("/")
            diary_file = open(f"{dir}/{day_num}-{month}-{year}", "x")
            diary_file.write(content)
            tl2.destroy()
        else:
            messagebox.showinfo("Diary", "Sorry but the date spcified is't found in the database or it not written yet ")
            tl2.destroy()
    
    def download_all():
        dir = filedialog.askdirectory() 
        data = tuple(c.execute("select * from diary"))
        for i in data:
            day_num, month, year = i[0].split("/")
            try:
                open(f"{dir}/{day_num}-{month}-{year}", "x").write(i[1])
            except FileExistsError:
                messagebox.showinfo("Diary", f"The file we are nameing already exists. File-name {i[0]} could not be copyied")
                continue
        tl2.destroy()
        
    day_sb = Spinbox(tl2, from_=1, to=31)
    month_sb = Spinbox(tl2, from_=1, to=12, command=day_change)
    year_sb = Spinbox(tl2, from_=2000 ,to=3000)
    enter_button = Button(tl2,  text="Enter", command=download)
    download_all_button = Button(tl2, text="Download all", command=download_all)
    date = ""
         
    day_sb.pack()
    month_sb.pack()
    year_sb.pack()
    enter_button.pack()
    download_all_button.pack()
    
    tl2.mainloop()
    
    
entered = True
if tuple(c.execute(f"Select * from diary where datetime='{datetime_create()[1]}'")) == ():
    entered = False
else: 
    entered = True
    
sc = scrolledtext.ScrolledText(root, width=500, height = 200)
starting_text= datetime_create()[0]
date_ = datetime_create()[1]
menu = Menu(root, tearoff=False)
actions_menu = Menu(menu, tearoff=False)

menu.add_cascade(menu=actions_menu, label="Actions")
actions_menu.add_command(label="Read dairy", command=fechter)
actions_menu.add_command(label="Format Database", command=format_data_base)
actions_menu.add_command(label="Download diary", command=download_db)
actions_menu.add_command(label="Enter dairy into database", command=insert_data)

root.config(menu=menu)
sc.pack()

if not entered:
    sc.insert(1.0, starting_text)
    
else:
    pass

root.mainloop()