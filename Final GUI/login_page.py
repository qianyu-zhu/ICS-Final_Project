import tkinter
import tkinter.messagebox
from chat_utils import *
from chat_client_class import *
import os


class GUI_Logged_in:

    def __init__(self, username):

        #-------------------------------------#
        #---------- Chat Initiating ----------#
        #-------------------------------------#

        import argparse
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()

        self.client = Client(args)
        self.logged_in = False
        self.client.do_input(username)
        self.client.run_chat(username)
        self.logged_in = self.client.login()

        #-------------------------------------#
        #---------- Chat Initiating ----------#
        #-------------------------------------#

        self.main_window = tkinter.Tk()
        self.main_window.geometry('750x400')
        self.main_window.title('Century Avenue No.1555 Chat')

        self.full_info = ''
        self.reading_position = 0

        self.top_frame = tkinter.Frame(self.main_window)
        self.mid_frame = tkinter.Frame(self.main_window)
        self.bot_frame = tkinter.Frame(self.main_window)

        #----- Top Frame Hello User -----#
        self.hello_label = tkinter.Label(self.top_frame, text='Hello {}'.format(username), font='Arial -30 bold')
        self.hello_label.pack()
        #----- Top Frame Hello User -----#

        #----- Mid Frame Info Box -----#
        self.output_msg = tkinter.StringVar()
        self.full_info = self.client.output()
        self.output_msg.set(self.full_info)
        self.info_label = tkinter.Label(self.mid_frame, textvariable=self.output_msg, height=18, width=60, bg='#FFFFF0')
        self.info_label.pack(side='top')

        #----- Mid Frame Info Box -----#

        #----- Bot Frame Text Input -----#
        self.quit_button = tkinter.Button(self.bot_frame, text='Quit', width=6, command=self.quit)
        self.quit_button.pack(side='left')
        self.my_msg_entry = tkinter.Entry(self.bot_frame, width=40)
        self.my_msg_entry.pack(side='left')
        self.send_button = tkinter.Button(self.bot_frame, text='Send', width=6, command=self.update_output)
        self.send_button.pack(side='left')
        self.up_button = tkinter.Button(self.bot_frame, text='↑', width=6, command=self.move_up)
        self.down_button = tkinter.Button(self.bot_frame, text='↓', width=6, command=self.move_down)
        self.up_button.pack(side='left')
        self.down_button.pack(side='left')

        #----- Bot Frame Text Input -----#

        self.top_frame.pack()
        self.mid_frame.pack()
        self.bot_frame.place(x=75, y=340)

        self.clock()

        self.main_window.mainloop()

        #-----------------------------------#
        #---------- Timely Update ----------#
        #-----------------------------------#

    def clock(self):                           # $$$ USER READING IN
        self.client.proc()
        sys_msg = self.client.output()
        if len(sys_msg) > 0:
            self.full_info += '\n' + sys_msg + '\n'
            # UPDATE LABEL
            offset = 0
            self.update_label(sys_msg, offset, 2)

        self.main_window.after(1000, self.clock)

        #-----------------------------------#
        #---------- Timely Update ----------#
        #-----------------------------------#
    # Auto downward moving, not to the bottom, easy to get out of sync
    def update_label(self, msg, offset=0, pad=0):  # msg handles self.client.output() and self.my_msg_entry.get()
        all_lines = self.full_info.split('\n')
        msg_list = msg.split('\n')
        if len(all_lines) == 18:
            if pad < 0 and self.reading_position == 0:
                pass
            else:
                self.reading_position += pad
        if len(all_lines) > 18:
            self.reading_position += len(msg_list) + 1
        # temporary adjustment, say for sonnet, offset = -10 to show the who poem from beginning, for admin notification, offset = -1 to allow another line saying Admin has done something
        self.reading_position += offset

        lines_displaying = all_lines[self.reading_position:self.reading_position + 17]
        lines_displaying = '\n'.join(lines_displaying) + '\n'

        self.output_msg.set(lines_displaying)


    # Auto move to the bottom when new message created
    def update_label(self, msg):
        all_lines = self.full_info.split('\n')
        msg_list = msg.split('\n')
        self.reading_position = (len(all_lines) - 9) * 2
        lines_displaying = all_lines[self.reading_position:self.reading_position + 9]
        lines_displaying = '\n\n'.join(lines_displaying)


    def move_label(self, k):  # msg handles self.client.output() and self.my_msg_entry.get()
        all_lines = self.full_info.split('\n')

        if len(all_lines) > 18:
            if k > 0:
                print('all_lines', len(all_lines))
                if self.reading_position < len(all_lines) - 10:
                    self.reading_position += k
            if k < 0:
                if self.reading_position > 0:
                    self.reading_position += k

        lines_displaying = all_lines[self.reading_position:self.reading_position + 17]
        lines_displaying = '\n'.join(lines_displaying)
        lines_displaying = '\n' + lines_displaying + '\n'
        self.output_msg.set(lines_displaying)
        print(self.reading_position)

    def update_output(self):  # $$$ USER WRITING OUT
        # Pass input to client
        if len(self.my_msg_entry.get()) > 0:
            # checking
            self.input = self.my_msg_entry.get()
            self.full_info += '\n' + self.input + '\n'
            self.client.do_input(self.input)
            # UPDATE LABEL
            offset = 0
            self.update_label(self.input, offset, -2)

            if not self.logged_in:
                self.logged_in = self.client.login()

            if self.logged_in and self.client.sm.get_state() != S_OFFLINE:
                print(True)
                self.client.proc()
                time.sleep(CHAT_WAIT)
                self.clock()
                #----------------------------------#
                #--------------- Game -------------#
                #----------------------------------#
                if self.input == 'snake':
                    self.snake()

                elif self.input == 'color':
                    self.color()

                #----------------------------------#
                #--------------- Game -------------#
                #----------------------------------#

            else:
                self.client.shutdown_chat()
                self.client.quit()
                self.quit()

        while self.my_msg_entry.get() != '':
            self.my_msg_entry.delete(0)

    def move_up(self):
        self.move_label(-2)

    def move_down(self):
        self.move_label(2)

    def quit(self):
        if self.client.sm.get_state() == S_CHATTING:
            self.client.do_input('bye')
            self.client.proc()
        self.client.quit()
        self.main_window.destroy()

    def snake(self):

        os.system("snakeGame.py")
        return

    def color(self):
        os.system("python3 color.py")
        return


if __name__ == '__main__':
    myGUI = GUI_Logged_in('TIGO')