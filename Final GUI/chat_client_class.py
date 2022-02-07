import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import tkinter as tk
import threading
import os

class Client:
    def __init__(self, args):
        self.peer = ''
        self.box_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        self.name = ''
        self.init_chat()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = SERVER if self.args.d is None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        # peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.box_input) > 0:
            my_msg = self.box_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def login_or_not(self, name):
        # my_msg, peer_msg = self.get_msgs()
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.name = name
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                return True
            elif response["status"] == 'duplicate':
                # self.system_msg += 'Duplicate username, try again'
                print('duplicate username')
                return False
        else:  # fix: dup is only one of the reasons
            return False

    def print_instructions(self):
        self.system_msg += menu

    # ==============================================================================
    # main processing loop
    # ==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)


class GUI(Client):

    # constructor method
    def __init__(self, args):
        # chat window which is currently hidden
        super().__init__(args)

        self.Window = tk.Tk()
        self.Window.withdraw()

        # login window
        self.login = tk.Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = tk.Label(self.login,
                            text="Please login to continue",
                            justify=tk.CENTER,
                            font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = tk.Label(self.login,
                                  text="Name: ",
                                  font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = tk.Entry(self.login,
                                  font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the curser
        self.entryName.focus()

        # create a Continue Button
        self.go = tk.Button(self.login,
                            text="CONTINUE",
                            font="Helvetica 14 bold",
                            command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        if self.login_or_not(name):
            self.login.destroy()
            self.layout()
#            os.system('python firstscreen.py')
            runchat = threading.Thread(target=self.run_chat)
            runchat.start()
        else:
            self.pls = tk.Label(self.login,
                                text="Duplicate username, try again",
                                justify=tk.CENTER,
                                font="Helvetica 14 bold")

            self.pls.place(relheight=0.15,
                           relx=0.2,
                           rely=0.07)

    def clock(self):
        hour = time.strftime('%H')
        minute = time.strftime('%M')
        second = time.strftime('%S')
        day = time.strftime('%A')

        self.clock_label.config(text=f'{day}   {hour}:{minute}:{second} ')
        self.clock_label.after(1000, self.clock)

    # The main layout of the chat
    def layout(self):
        # to show chat window
        self.Window.deiconify()
        self.Window.title("NYU CHATROOM")

        canvas = tk.Canvas(self.Window, height=500, width=600)
        canvas.pack()

        background_image = tk.PhotoImage(file='/Users/zhuqianyu/Desktop/UP3_2/nyushanghai.png')
        background_label = tk.Label(self.Window)
        background_label.image = background_image
        background_label.configure(image=background_image)
        background_label.place(relwidth=1, relheight=1)

        # label of a clock to show time
        self.clock_label = tk.Label(self.Window, text='', font='Helvetica 15')
        self.clock_label.place(relx=0.642, rely=0.055)

        self.clock()

        # frame to displays messages
        frame = tk.Frame(self.Window, bg='#80c1ff', bd=10)
        frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.6, anchor='n')

        # frame to type messages
        lower_frame = tk.Frame(self.Window, bg='#80c1ff', bd=5)
        lower_frame.place(relx=0.5, rely=0.75, relwidth=0.75, relheight=0.1, anchor='n')

        # entry to type in
        self.entryMsg = tk.Entry(lower_frame, font=40)
        self.entryMsg.place(relwidth=0.75, relheight=1)
        self.entryMsg.focus()

        # the 'send' button
        self.buttonMsg = tk.Button(lower_frame, text="send", font=40,
                                   command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.8, relheight=1, relwidth=0.2)

        # the quit button
        self.buttonQuit = tk.Button(self.Window, text="quit", font=40,
                                   command=lambda: self.quitbutton_act())
        self.buttonQuit.place(relx=0.6, rely=0.055, anchor='n')
        # the Snake Game button
        self.buttonGame1 = tk.Button(self.Window, text="Snake Game", font="Helvetica 13 bold", fg='#DC143C',
                                     command=lambda: self.sendButton("Snake Game"))
        self.buttonGame1.place(relx=0.28, rely=0.055, anchor='n')

        # the Go Bang button
        self.buttonGame2 = tk.Button(self.Window, text="Go Bang", font="Helvetica 13 bold", fg='#DC143C',
                                     command=lambda: self.sendButton("Go Bang"))
        self.buttonGame2.place(relx=0.415, rely=0.055, anchor='n')

        # the Kill Final button
        self.buttonGame3 = tk.Button(self.Window, text="Kill Final", font="Helvetica 12 bold", fg='#DC143C',
                                     command=lambda: self.sendButton("Kill Final"))
        self.buttonGame3.place(relx=0.52, rely=0.055, anchor='n')

        # to display text
        self.textCons = tk.Text(frame,
                                width=20,
                                height=2,
                                font="Helvetica 14",
                                padx=5,
                                pady=5)

        self.textCons.place(relheight=1,
                            relwidth=1)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=tk.DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def quitbutton_act(self):
        self.sendButton('q')

    def two_player_game_act(self):
        self.sendButton('game')

    # function to receive messages
    def output(self):
        if len(self.system_msg) > 0:
            self.textCons.config(state=tk.NORMAL)
            self.textCons.insert(tk.END,
                                 self.system_msg + "\n\n")
            self.textCons.config(state=tk.DISABLED)
            self.textCons.see(tk.END)
            self.system_msg = ''

    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED)
        while True:
            self.box_input.append(self.msg)  # no need for lock, append is thread safe
            break

    def run_chat(self):
        self.system_msg += 'Welcome to ICS chat, ' + self.get_name() + '!'
        self.print_instructions()
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()
        self.Window.quit()

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

