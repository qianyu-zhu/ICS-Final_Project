import tkinter
import tkinter.messagebox
# from chat_client_class import *
from GUI_Logged_in_Page import *
from chat_client_class import *

from tkinter import *
from tkinter import messagebox


class LogInterface:
    def __init__(self):
        #---- Main Window ----#
        self.main_window = tkinter.Tk()
        self.main_window.title('Welcome to TiGo Chat!')
        self.main_window.geometry('450x300')

        #---- Welcome Image ----#
        self.canvas = tkinter.Canvas(self.main_window, height=200, width=500)
        image_file = tkinter.PhotoImage(file='logo.gif')
        image = self.canvas.create_image(0, 10, anchor='nw', image=image_file)

        self.canvas.pack(side='top')

        #---- User Info ----#
        self.userlabel = tkinter.Label(self.main_window, text='User name:')
        self.password_label = tkinter.Label(self.main_window, text='Password:')

        self.userlabel.place(x=50, y=150)
        self.password_label.place(x=50, y=190)

        #---- User Entry ----#
        self.username_var = tkinter.StringVar()
        # self.username.set('Input your user name here')
        self.userpass_var = tkinter.StringVar()

        self.username_entry = tkinter.Entry(self.main_window, textvariable=self.username_var)
        self.user_pass = tkinter.Entry(self.main_window, textvariable=self.userpass_var, show='*')

        self.username_entry.place(x=160, y=150)
        self.user_pass.place(x=160, y=190)

        #---- Buttons ----#
        self.login_b = tkinter.Button(self.main_window, text='Login', command=self.user_login)
        self.login_b.place(x=170, y=230)

        self.sign_up_b = tkinter.Button(self.main_window, text='Sign up', command=self.user_sign_up)
        self.sign_up_b.place(x=270, y=230)

#----------------------------------------------------#
        # self.users_info: The passwords have been transfered to the server side for security improvement
#----------------------------------------------------#
        # establishing temporary connection with server through the name of logger
        import argparse
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()

        self.client = Client(args)
        self.logged_in = False
        self.client.do_input('logger')
        self.client.run_chat('logger')
        self.logged_in = self.client.login()
        print('logger born', self.logged_in)
        tkinter.mainloop()

    def user_login(self):
        self.user_name = self.username_var.get()
        self.user_pass = self.userpass_var.get()
        # send out this two info
        msg = json.dumps({"action": "login", "name-pass": self.user_name + ',' + self.user_pass})
        self.client.send(msg)
        response = json.loads(self.client.recv())
        if response["status"] == 'okay':
            print('User verified by the server')
            print('The login proxy logger has been killed by server, salute to logger!')
            self.main_window.destroy()
            self.new_window = GUI_Logged_in(self.user_name)  # Re login as the real user. Right now the hacker can still use this method to bypass the login process, but with RSA added, this part is much safer.
            # S_LOGGEDIN
        elif response["status"] == 'notFound':
            self.sign_up = tkinter.messagebox.askyesno('Welcome', 'User name does not exist.\nSign up?')
            if self.sign_up:
                self.user_sign_up()

        elif response["status"] == 'duplicate':
            tkinter.messagebox.showinfo('Error!', 'This user has already logged in, try again')

        elif response["status"] == 'incorrect':
            tkinter.messagebox.showinfo('Error!', 'Password and name don\'t match, try again')

        '''
        # $$$$$$$$$$$$$$$$$$
        #---- Checking with Server ----#
        if self.user_name in self.users_info:
            if self.user_pass == self.users_info[self.user_name]:
                self.init_chat = tkinter.messagebox.askyesno('Welcome!', 'How are you? ' + self.user_name + '\nInitiate Chat?')
                if self.init_chat:
                    #---------------Initiating Chat---------------#
                    #---------------Initiating Chat---------------#
                    self.main_window.destroy()
                    self.new_window = GUI_Logged_in(self.user_name)
                    #---------------Initiating Chat---------------#
                    #---------------Initiating Chat---------------#
            else:
                tkinter.messagebox.showinfo('Error!', 'Password Incorrect!')
        else:
            self.sign_up = tkinter.messagebox.askyesno('Welcome', 'User name does not exist.\nSign up?')
        '''

    def user_sign_up(self):

        def new_user_sign_up():
            nn = new_name.get()
            np = new_pwd.get()
            npc = new_pwd_confirm.get()
            if nn.strip() and np.strip() and npc.strip():
                if np != npc:
                    tkinter.messagebox.showerror('Error', 'Password does not match!')
                else:
                    # send out this two new info to register at server
                    msg = json.dumps({"action": "register", "name-pass": nn + ',' + np})
                    self.client.send(msg)
                    print('sending registration info')
                    response = json.loads(self.client.recv())
                    print('response to registration comes back from server: ', response)
                    if response["status"] == 'okay':
                        tkinter.messagebox.showinfo('Welcome', 'You have successfully signed up!')
                        self.sign_up_window.destroy()

                    elif response["status"] == 'duplicate':
                        tkinter.messagebox.showerror('Error', 'User name already exist!')
            else:
                tkinter.messagebox.showerror('Error', 'Sorry, you can\'t leave a blank name or password')
#----------------------------------------------------#
# $$$$$$$$$$$$$$$$$$
            # if nn in self.users_info:
            #     tkinter.messagebox.showerror('Error', 'User name already exist!')

            # else:
            #     self.users_info[nn] = np
            #     tkinter.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            #     self.sign_up_window.destroy()


#----------------------------------------------------#

        self.sign_up_window = tkinter.Toplevel(self.main_window)
        self.sign_up_window.geometry('350x200')
        self.sign_up_window.title('Sign up')

        # Username #
        new_name = tkinter.StringVar()
        tkinter.Label(self.sign_up_window, text='User name:').place(x=10, y=10)
        entry_new_name = tkinter.Entry(self.sign_up_window, textvariable=new_name)
        entry_new_name.place(x=150, y=10)

        # Password #
        new_pwd = tkinter.StringVar()
        tkinter.Label(self.sign_up_window, text='Password:').place(x=10, y=50)
        entry_new_pwd = tkinter.Entry(self.sign_up_window, textvariable=new_pwd, show='*')
        entry_new_pwd.place(x=150, y=50)

        # Confirm Password #
        new_pwd_confirm = tkinter.StringVar()
        tkinter.Label(self.sign_up_window, text='Confirm password:').place(x=10, y=90)
        entry_new_pwd_confirm = tkinter.Entry(self.sign_up_window, textvariable=new_pwd_confirm, show='*')
        entry_new_pwd_confirm.place(x=150, y=90)

        # Sign up Button #
        confirm_sign_up = tkinter.Button(self.sign_up_window, text='Sign up', command=new_user_sign_up)
        confirm_sign_up.place(x=150, y=130)


if __name__ == '__main__':
    login = LogInterface()
