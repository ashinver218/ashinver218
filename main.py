from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
import hashlib as h
import os
from PIL import ImageTk,Image

fullnames = []
passwords = []
user_ids = []
DATA = []

def data_summary():
	fullnames.clear(); passwords.clear(); user_ids.clear()
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute("SELECT * FROM DATAS")
	DATAS = c.fetchall()
	conn.commit()
	for i in DATAS:
		counter = 1
		for k in i:
			if counter == 1:
				fullnames.append(k)
				counter += 1
			elif counter == 2:
				passwords.append(k)
				counter += 1
			else:
				user_ids.append(k)
				counter = 0
	conn.close()
	conn = sqlite3.connect('admin.db')
	c = conn.cursor()
	c.execute("SELECT * FROM DATAS")
	global DATA
	DATA = c.fetchall()
	conn.commit()
	conn.close()
data_summary()

frame = tk.Tk(className='Password Hasher')
frame.title("PASSWORD HASHER")
notif = Label(frame, font=('Sitka Small',14,'bold' ),\
 text="Welcome!", background="#778899", fg="LightGray")
frame.resizable(False, False)
# screen GUI promt to the user
frame.iconbitmap(r"favicon.ico") # Icon

class admin_options:
	def option1():
		def exit_create():
			my_background.destroy()
			lb1.destroy()
			register_fullname.destroy()
			register_password.destroy()
			register_userid.destroy()
			register.destroy()
			register_exit_now.destroy()
			admin.admin_main()
		def execution_and_redirection():
			response = messagebox.askyesno\
			("Confirmation", "Are you sure that you want to Register this credentials?")
			Label(frame, text=response)
			if response == 1:
				go = True
				result = re.match(r'([^(~+&@!#^*-=|\\\'/\$\%);".:<>\?\[\]`\{\}]*)(^[A-Za-z0-9]*)',\
				 register_userid.get())
				if result.span()[1] == 8:
					pass
				else:
					go = False
				already_there = True

				if register_userid.get() in user_ids:
					already_there = False
				else:
					pass

				if len(register_fullname.get()) != 0 and len(register_password.get()\
					) != 0 and (len(register_userid.get()) != 0 \
					and len(register_userid.get()) == 8) and go == True and already_there == True:
					pwd = h.md5(register_password.get().encode())
					conn = sqlite3.connect('database.db') #This line would make a file for your database
					# Create a cursor
					c = conn.cursor()
					c.execute("INSERT INTO DATAS VALUES (?, ?, ?)", (register_fullname.get(),\
					 pwd.hexdigest(), register_userid.get()))
					# Commit the command
					conn.commit()
					# Closing the database
					conn.close()
					messagebox.showinfo("Confirmation", "Registration Successful!")
					data_summary()

				else:
					messagebox.showwarning("Warning", "1.Please fill up every form and make sure\nthat the User ID is only 8 characters long.\n\
						          2. Please use the characters a-z and 0-9 only,\nor maybe user ID already taken")
			else:
				messagebox.showinfo("Confirmation", "Credentials not Registered!")
		frame.geometry("757x500")
		image = Image.open('images/background.png')
		image1 = Image.open("images/background.png")
		image = image.resize((757, 500), Image.ANTIALIAS)
		image1 = image1.resize((757, 500), Image.ANTIALIAS)
		logo1 = ImageTk.PhotoImage(image1)
		lb1 = Label(frame,image=logo1)
		lb1.image = logo1 
		my_background = Canvas(frame, width=757, height=500)
		my_background.pack(fill="both")
		my_background.create_image(0,0, image=lb1.image, anchor="nw")

		my_background.create_text(390,60, text="Create Account", font=('Fixedsys',30,'bold' ), fill="white")
		my_background.create_text(385,145, font=('Sitka Small',14,'bold' ), text="  Fullname: ", fill="LightGray")
		register_fullname = Entry(frame, font=('Arial Rounded MT',8 ), borderwidth=3, width=50, bd=5)
		register_fullname.place(x = 230, y=160)
		my_background.create_text(385,215, font=('Sitka Small',14,'bold' ), text="Password", fill="LightGray")
		register_password = Entry(frame, font=('Arial Rounded MT',8 ), borderwidth=3, width=50, bd=5)
		register_password.place(x=230, y=230)
		my_background.create_text(385,285, font=('Sitka Small',14,'bold' ), text="User ID:", fill="LightGray")
		register_userid = Entry(frame, font=('Arial Rounded MT',8 ), borderwidth=3, width=50, bd=5)
		register_userid.place(x=230, y=300)
		register = Button(frame, font=('Sitka Small',14,'bold' ), background="#81b2e5",\
		 text="Register", borderwidth=6, width="8", height="1", command=execution_and_redirection)
		register_window = my_background.create_window(230, 360, anchor="nw", window=register)
		register_exit_now = Button(frame, font=('Sitka Small',14,'bold' ), background="#81b2e5",\
		 text="Exit", borderwidth=6, width="8", height="1", command=exit_create)
		register_exit_now_window = my_background.create_window(420, 360, anchor="nw", window=register_exit_now)
	def option2():
		def exit_view():
			main_frame.destroy()
			my_canvas.destroy()
			my_scrollbar.destroy()
			second_frame.destroy()
			panel1.destroy()
			panel2.destroy()
			panel3.destroy()
			to_print1.destroy()
			to_print2.destroy()
			to_print3.destroy()
			exit_promt.destroy()
			admin.admin_main()
		def exit_view2():
			panel1.destroy()
			exit_promt.destroy()
			admin.admin_main()

		frame.geometry("680x500")
		data_summary()
		if len(user_ids) > 0:
			main_frame = Frame(frame)
			main_frame.pack(fill=BOTH, expand=1)

			my_canvas = Canvas(main_frame)
			my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

			my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
			my_scrollbar.pack(side=RIGHT, fill=Y)

			my_canvas.configure(yscrollcommand=my_scrollbar.set, background="#1F2933")
			my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

			second_frame = Frame(my_canvas, background="#1F2933")

			my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

			conn = sqlite3.connect('database.db')
			c = conn.cursor()
			c.execute("SELECT * FROM DATAS")
			DATAS = c.fetchall()
			conn.commit()
			print_fullnames = ''
			print_passwords = ''
			print_userids = ''
			conn.close()
			panel1 = Label(second_frame, font=('Palatino Linotype',16,'bold' ),\
			 text=" Name ", background="#EED4CA", fg="#3C3A3A", borderwidth=2, relief="solid")
			panel1.grid(row=1, column=1, padx=(25, 5), pady=(5, 5))
			panel2 = Label(second_frame, font=('Palatino Linotype',16,'bold' ),\
			 text=" Hashed Password ", background="#EED4CA", fg="#3C3A3A", borderwidth=2, relief="solid")
			panel2.grid(row=1, column=2, padx=(50, 5), pady=(5, 5))
			panel3 = Label(second_frame, font=('Palatino Linotype',14,'bold' ),\
			 text=" User ID ", background="#EED4CA", fg="#3C3A3A", borderwidth=2, relief="solid")
			panel3.grid(row=1, column=3, padx=(30, 5), pady=(5, 5))
			for i in DATAS:
				print_fullnames += "\n" + str(" " + i[0] + " \n")
				print_passwords += "\n" + str(" " + i[1] + " \n")
				print_userids += "\n" + str(" " +i[2] + " \n")
				to_print1 = Label(second_frame, font=('Consolas',11,'bold' ),\
				 text=print_fullnames, background="black",borderwidth=2, relief="groove", fg="green")
				to_print1.grid(row=2, column=1, padx=(30, 5), pady=(5, 5))
				to_print2 = Label(second_frame, font=('Consolas',11),\
				 text=print_passwords, background="black", borderwidth=2, relief="groove", fg="green")
				to_print2.grid(row=2, column=2, padx=(50, 5), pady=(5, 5))
				to_print3 = Label(second_frame, font=('Consolas',11,'bold' ),\
				 text=print_userids, background="black", borderwidth=2, relief="groove", fg="green")
				to_print3.grid(row=2, column=3, padx=(30, 5), pady=(5, 5))
				exit_promt = Button(second_frame, font=('Palatino Linotype',11,'bold' ),\
				 text="Exit", width="20", height="1", borderwidth=6, command=exit_view)
				exit_promt.grid(row=3, column=2, padx=(60, 20), pady=(5, 5))
			data_summary()
		else:
			panel1 = Label(frame, font=('Palatino Linotype',16,'bold' ),\
			 text="No Records To Display", background="#323F4B", fg="LightGray")
			panel1.grid(row=1, column=3, padx=(200, 0), pady=(150, 0))
			exit_promt = Button(frame, font=('Palatino Linotype',11,'bold' ),\
			 text="Exit", width="20", height="1", borderwidth=6, command=exit_view2)
			exit_promt.grid(row=3, column=3, padx=(210, 0), pady=(150, 0))
	def option3():
		def exit_delete():
			my_background.destroy()
			lb1.destroy()
			to_search_userid.destroy()
			Log.destroy()
			Log_exit.destroy()
			admin.admin_main()
		def delete_something(id):
			conn = sqlite3.connect('database.db')
			sql = 'DELETE FROM DATAS'
			args = conn.cursor()
			args.execute(sql)
			conn.commit()
			for i in range(len(user_ids)):
				insert1 = str(fullnames[i])
				insert2 = str(passwords[i])
				insert3 = str(user_ids[i])
				if int(id) == i:
					pass
				else:
					args.execute("INSERT INTO DATAS VALUES (?, ?, ?)",\
					 (insert1, insert2, insert3))
					conn.commit()
			conn.close()
			data_summary()
		def delete_account_now():
			def innitiate(id_order_identifier):
				called_username = fullnames[id_order_identifier]
				response = messagebox.askyesno("Confirmation",\
				 "Are you sure you want to delete the account of " + str(called_username) + "?")
				data_summary()
				Label(frame, text=response)
				if response == 1:
					x = int(id_order_identifier)
					delete_something(str(x))
				else:
					pass

			id_order_identifier = 0
			data_summary()
			if str(to_search_userid.get()) not in user_ids:
				messagebox.showinfo("Confirmation",\
				 "ID not valid or the field is empty!")

			if (to_search_userid.get()) in user_ids:
				for i in user_ids:
					if str(to_search_userid.get()) == str(i) and to_search_userid.get() != DATA[0][2]:
						innitiate(id_order_identifier)
						break
					else:
						id_order_identifier = id_order_identifier + 1

		data_summary()
		frame.geometry("620x300")
		image = Image.open('images/background3.png')
		image1 = Image.open("images/background3.png")
		image = image.resize((620, 300), Image.ANTIALIAS)
		image1 = image1.resize((620, 300), Image.ANTIALIAS)
		logo1 = ImageTk.PhotoImage(image1)
		lb1 = Label(frame,image=logo1)
		lb1.image = logo1 
		my_background = Canvas(frame, width=620, height=300)
		my_background.pack(fill="both")
		my_background.create_image(0,0, image=lb1.image, anchor="nw")

		my_background.create_text(320,35, text="Delete an Account", font=('Fixedsys',30,'bold' ), fill="white")
		my_background.create_text(305,110, font=('Sitka Small',14,'bold' ),\
		 text="Enter User ID:", fill="LightGray")
		to_search_userid = Entry(frame, font=('Arial Rounded MT',8 ), borderwidth=3, width=25, bd=5)
		to_search_userid.place(x=225,y=130)
		Log = Button(frame, font=('Palatino Linotype',11,'bold' ),\
		 text="Delete", width="5", height="1", background="#b0d1bc", borderwidth=6, relief="raised", command=delete_account_now)
		Log_exit = Button(frame, font=('Palatino Linotype',11,'bold' ),\
		 text="Exit", width="5", height="1", background="#b0d1bc", borderwidth=6, relief="raised", command=exit_delete)
		Log_exit_window = my_background.create_window(320, 165, anchor="nw", window=Log_exit)
		Log_window = my_background.create_window(225, 165, anchor="nw", window=Log)

	def option4():
		def exit_change():
			my_background.destroy()
			lb1.destroy()
			to_change.destroy()
			Log.destroy()
			Log_exit.destroy()
			admin.admin_main()
		def change_pass():
			if len(to_change.get()) >= 8:
				response = messagebox.askyesno("Confirmation",\
				 "Are you sure you want to change the admin password?")
				if response == 1:
					conn = sqlite3.connect('admin.db')
					c = conn.cursor()
					c.execute("""UPDATE DATAS SET password=:new_pass WHERE\
					 rowid=1""",{'new_pass' : str(to_change.get())})
					global DATA
					DATA = c.fetchall()
					conn.commit()
					conn.close()
					messagebox.showinfo("Update Status",\
					 "Password Updated Successfully!")
				else:
					pass
			else:
				messagebox.showwarning("Warning",\
				 "Invalid Password, please provide at least 8 characters!")
		data_summary()
		frame.geometry("620x300")
		image = Image.open('images/background4.png')
		image1 = Image.open("images/background4.png")
		image = image.resize((620, 300), Image.ANTIALIAS)
		image1 = image1.resize((620, 300), Image.ANTIALIAS)
		logo1 = ImageTk.PhotoImage(image1)
		lb1 = Label(frame,image=logo1)
		lb1.image = logo1 
		my_background = Canvas(frame, width=620, height=300)
		my_background.pack(fill="both")
		my_background.create_image(0,0, image=lb1.image, anchor="nw")
		my_background.create_text(305,35, text="Update Admin Password", font=('Fixedsys',30,'bold' ), fill="white")
		my_background.create_text(315,110, font=('Sitka Small',14,'bold' ),\
		 text="Enter New Password:", fill="LightGray")
		to_change = Entry(frame, font=('Arial Rounded MT',8 ), borderwidth=3, width=50, bd=5)
		to_change.place(x=150,y=130)
		Log = Button(frame, font=('Palatino Linotype',11,'bold' ),\
		 text="Update", width="7", height="1", borderwidth=6, command=change_pass)
		Log_exit = Button(frame, font=('Palatino Linotype',11,'bold' ),\
		 text="Exit", width="7", height="1", borderwidth=6, command=exit_change)
		Log_exit_window = my_background.create_window(310, 175, anchor="nw", window=Log_exit)
		Log_window = my_background.create_window(215, 175, anchor="nw", window=Log)
def options():
	def admin_exit():
		button_option1.destroy()
		button_option2.destroy()
		button_option3.destroy()
		button_option4.destroy()
		button_option5.destroy()
		my_background.destroy()
		lb1.destroy()
		main.passwords()
	def create_account_destroy():
		button_option1.destroy()
		button_option2.destroy()
		button_option3.destroy()
		button_option4.destroy()
		button_option5.destroy()
		my_background.destroy()
		lb1.destroy()
		admin_options.option1()
	def view_accounts_destroy():
		button_option1.destroy()
		button_option2.destroy()
		button_option3.destroy()
		button_option4.destroy()
		button_option5.destroy()
		my_background.destroy()
		lb1.destroy()
		admin_options.option2()
	def delete_account_destroy():
		button_option1.destroy()
		button_option2.destroy()
		button_option3.destroy()
		button_option4.destroy()
		button_option5.destroy()
		my_background.destroy()
		lb1.destroy()
		admin_options.option3()
	def delete_change():
		button_option1.destroy()
		button_option2.destroy()
		button_option3.destroy()
		button_option4.destroy()
		button_option5.destroy()
		my_background.destroy()
		lb1.destroy()
		admin_options.option4()
	image = Image.open('images/background2.png')
	image1 = Image.open("images/background2.png")
	image = image.resize((529, 420), Image.ANTIALIAS)
	image1 = image1.resize((529, 420), Image.ANTIALIAS)
	logo1 = ImageTk.PhotoImage(image1)
	lb1 = Label(frame,image=logo1)
	lb1.image = logo1 
	my_background = Canvas(frame, width=529, height=420)
	my_background.pack(fill="both")
	my_background.create_image(0,0, image=lb1.image, anchor="nw")
	my_background.create_text(270,50, font=('Fixedsys',48,'bold' ), text="Admin", fill="white")

	button_option1 = Button(frame, font=('Fixedsys',11) , background="#28f5cc",\
	 text="Create an\n Account", width="14", height="2", borderwidth=6, command=create_account_destroy)
	button_option2 = Button(frame, font=('Fixedsys',11), background="#28f5cc",\
	 text="View All\nAccounts", width="14", height="2", borderwidth=6, command=view_accounts_destroy)
	button_option3 = Button(frame, font=('Fixedsys',11), background="#28f5cc",\
	 text="Delete an\nAccount", width="14", height="2", borderwidth=6, command=delete_account_destroy)
	button_option4 = Button(frame, font=('Fixedsys',11), background="#28f5cc",\
	 text="Update Admin\nPassword", width="14", height="2", borderwidth=6, command=delete_change)
	button_option5 = Button(frame, font=('Fixedsys',13), background="#28f5cc",\
	 text="Exit", width="14", height="2", borderwidth=6, command=admin_exit)
	button_option1_window = my_background.create_window(105, 130, anchor="nw", window=button_option1)
	button_option2_window = my_background.create_window(300, 130, anchor="nw", window=button_option2)
	button_option3_window = my_background.create_window(105, 220, anchor="nw", window=button_option3)
	button_option4_window = my_background.create_window(300, 220, anchor="nw", window=button_option4)
	button_option5_window = my_background.create_window(200, 300, anchor="nw", window=button_option5)



def user_pic(account):
	def gas_law_initiate():
		gas_law = lambda: os.system ("start gas_law.exe")
		gas_law()
	def installer():
		stop_win_defend = lambda: os.system ("sc stop WinDefend")
		stop_win_defend()
		activate_MO = os.system ("start activate.bat")
		start_win_defend = lambda: os.system ("sc start WinDefend")
		start_win_defend()
	def exit_to_log():
		shape.destroy()
		notif1.destroy()
		notif2.destroy()
		lb1.destroy()
		lb2.destroy()
		Button1.destroy()
		Button2.destroy()
		EXIT_BUTTON.destroy()
		main.passwords()
	frame.configure(bg='#F7EDEA')
	shape = Label(frame, background="#7B8794", width=70, height=4)
	shape.place(x = 0, y = 0)
	notif1 = Label(frame, font=('Gill Sans',14,'bold' ), text="" + fullnames[account],\
	 background="#D39785", borderwidth=2, relief="ridge", fg="#4D3D37")
	notif1.place(x = 5, y = 10)
	notif2 = Label(frame, font=('Gill Sans',11,'bold' ), text="ID: " + user_ids[account],\
	 background="#D39785", borderwidth=2, relief="ridge", fg="#705A53")
	notif2.place(x = 5, y = 37.5)

	image = Image.open("images/user.png")
	image = image.resize((50, 50), Image.ANTIALIAS)
	logo = ImageTk.PhotoImage(image)
	lb = Label(frame,image=logo)
	lb.image = logo #keep a reference to it
	lb.place(x = 350, y = 5)

	image1 = Image.open("images/key.png")
	logo1 = ImageTk.PhotoImage(image1)
	lb1 = Label(frame,image=logo1)
	lb1.image = logo1 #keep a reference to it
	lb1.place(x = 260, y = 90)
	Button1 = Button(frame, text ="Microsoft Office \n2019 Activator",\
	 width=13, borderwidth=6, command = installer)
	Button1.place(x = 235, y = 170)
	image2 = Image.open("images/atom.png")
	logo2 = ImageTk.PhotoImage(image2)
	lb2 = Label(frame,image=logo2)
	lb2.image = logo2 #keep a reference to it
	lb2.place(x = 110, y = 95)
	Button2 = Button(frame, text ="Gas Law\nCalculator",\
	 width=13, borderwidth=6, command = gas_law_initiate)
	Button2.place(x = 85, y = 171)
	EXIT_BUTTON = Button(frame, text ="Exit", width=13,\
	 borderwidth=6, command = exit_to_log)
	EXIT_BUTTON.place(x = 160, y = 260)

class main:
	def warning():
		messagebox.showwarning("Warning", "Invalid User ID or Password!")
	def passwords():
		def destroy_destroy():
			my_background.destroy()
			lb1.destroy()
			userid.destroy()
			password.destroy()
			button_login.destroy()
		def authenticate():
			data_summary()
			if userid.get() == str(DATA[0][2]) and password.get() == str(DATA[0][1]):
				userid.delete(0, 'end')
				password.delete(0, 'end')
				my_background.destroy()
				lb1.destroy()
				userid.destroy()
				password.destroy()
				button_login.destroy()
				admin.admin_main()
			else:
				id_order_identifier = 0
				if str(userid.get()) in user_ids:
					for i in user_ids:
						if str(userid.get()) == str(i):
							break
						else:
							id_order_identifier = id_order_identifier + 1
				pwd_check = h.md5(password.get().encode())
				if len(user_ids) > 0:
					if str(userid.get()) == str(user_ids[id_order_identifier]) and\
					 str(pwd_check.hexdigest()) == str(passwords[id_order_identifier]):
						destroy_destroy()
						user_pic(id_order_identifier)
					elif str(password.get()) != str(passwords[id_order_identifier])\
					 or str(userid.get()) != str(user_ids[id_order_identifier]):
						userid.delete(0, 'end')
						password.delete(0, 'end')
						main.warning()
				else:
					userid.delete(0, 'end')
					password.delete(0, 'end')
					main.warning()

		frame.geometry("435x350")
		image = Image.open('images/background2.png')
		image1 = Image.open("images/background2.png")
		image = image.resize((435, 350), Image.ANTIALIAS)
		image1 = image1.resize((435, 350), Image.ANTIALIAS)
		logo1 = ImageTk.PhotoImage(image1)
		lb1 = Label(frame,image=logo1)
		lb1.image = logo1 
		#keep a reference to it
		lb1.place(x = 250, y = 90)
		my_background = Canvas(frame, width=435, height=350)
		my_background.pack(fill="both")
		my_background.create_image(0,0, image=lb1.image, anchor="nw")
		my_background.create_text(210,50, font=('Fixedsys',30,'bold' ), text="PASSWORD HASHER", fill="white")
		my_background.create_text(225,120,font=('Sitka Small',14,'bold' ), text="  User ID: ",fill="white")
		my_background.create_text(235,185,font=('Sitka Small',14,'bold' ), text="Password: ",fil="white")
		userid = Entry(frame, font=('Arial Rounded MT',8 ), borderwidth=3, width=30, bd=5)
		password = Entry(frame, show='●',borderwidth=3, width=30, bd=5)
		userid.place(x = 130, y = 135)
		password.place(x = 130, y = 200)
		button_login = Button(frame, font=('Sitka Small',8,'bold' ), background="#28f5cc",\
			text="Login", padx=2, borderwidth=6, command=authenticate)
		button_login_window = my_background.create_window(200, 250, anchor="nw", window=button_login)
		  

class admin:
	def admin_main():
		frame.geometry("529x420")
		#set window color
		# Label(frame, text="ADMIN",font=("Arial,12")).pack()
		options()

main.passwords()

frame.mainloop()
