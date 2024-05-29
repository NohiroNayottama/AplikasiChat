import customtkinter as ctk
from tkinter import END

from threading import Thread

import time # untuk waktu

import datetime #untuk waktu atau hari

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1024x720')
        self.title('Aplikasi Chatting')

        self.bind('<Return>',self.bt_send_com)
        
        self.list_persons=[]
        self.list_chat=[]
        self.list_frames=[]
        self.list_labels_info=[]
        self.list_rec={}

        #variabel nama dan index chat-1
        self.my_name=''
        self.index_chat=-1

        self.index_mode=0
        ## 0 --> text
        ## 1 --> record suara
        ## 2 --> stop record suara

        self.get_chats_Net()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)

        self.upperFrame = ctk.CTkFrame(self,corner_radius=0,fg_color='#FFFFFF')
        self.upperFrame.grid(row=0,column=0,columnspan=2,sticky='nswe')

        #bagian atas (chatapp dan nama pengguna)
        self.upperFrame.grid_rowconfigure(0, weight=1)
        self.upperFrame.grid_columnconfigure((0,2,3), weight=0)
        self.upperFrame.grid_columnconfigure(1, weight=1)

        #############################
        self.ch = ctk.CTkLabel(self.upperFrame, text=self.my_name[0],font=('Helvetica',20,'bold'),height=30,width=30,fg_color='#037562',text_color='white',corner_radius=5)
        self.ch.grid(row=0,column=3,padx=10,pady=10)
        self.lbl_text=ctk.CTkLabel(self.upperFrame, text=self.my_name,font=('Helvetica',16,'bold'))
        self.lbl_text.grid(row=0,column=2,pady=5,sticky='e')
        #############################

        #tombol logout
        self.bt_logOut = ctk.CTkButton(self.upperFrame, text='Logout',width=50,height=20,command=self.bt_logout_com)
        self.bt_logOut.grid(row=0,column=1,sticky='ws',pady=5)

        #logo Chats
        self.lblLogo = ctk.CTkLabel(self.upperFrame,text='Chats',font=('Helvetica',22,'bold'))
        self.lblLogo.grid(row=0,column=0,padx=10,pady=10)

        #frame chat sebelah kiri
        self.leftFrame = ctk.CTkScrollableFrame(self,fg_color='#FFFFFF',corner_radius=0)
        self.leftFrame.grid(row=1,column=0,sticky='nswe')

        self.leftFrame.grid_columnconfigure(0, weight=1)

        #frame chat sebelah kanan
        self.rightFrame = ctk.CTkFrame(self,fg_color='transparent',corner_radius=0)
        self.rightFrame.grid(row=1,column=1,sticky='nswe')

        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure((0,2,3), weight=0)
        self.rightFrame.grid_rowconfigure(1, weight=1)

        #bagian nama penerima chat
        self.headerFrame = ctk.CTkFrame(self.rightFrame,corner_radius=0,fg_color='#f0f2f5',height=0)
        self.headerFrame.grid(row=0,column=0,sticky='nswe')

        self.headerFrame.grid_rowconfigure(0, weight=1)
        self.headerFrame.grid_columnconfigure(0, weight=0)
        self.headerFrame.grid_columnconfigure(1, weight=1)

        #self.lblChatName = ctk.CTkLabel(self.headerFrame,text='Nohiro',font=('Helvetica',20,'bold'))
        #self.lblChatName.grid(row=0,column=0,sticky='w',padx=10,pady=5)

        self.chatFrame = ctk.CTkScrollableFrame(self.rightFrame,corner_radius=0,fg_color='#efeae2') #wallpaper
        self.chatFrame.grid(row=1,column=0,sticky='nswe')
        self.chatFrame.grid_columnconfigure(0, weight=1)

        self.footerFrame = ctk.CTkFrame(self.rightFrame,corner_radius=0,height=0)
        self.footerFrame.grid(row=3,column=0,sticky='nswe')

        self.footerFrame.grid_rowconfigure(0, weight=1)
        self.footerFrame.grid_columnconfigure(0, weight=1)
        self.footerFrame.grid_columnconfigure(1, weight=0)

        self.load_chats(self.list_persons)
        self.init_chat(None,self.index_chat,self.list_chat[self.index_chat])#,e,index,list_chat

    #fungsi logout
    def bt_logout_com(self):
        pass

    #fungsi kirim pesan
    def bt_send_com(self,e=None):
        ent_user = self.ent.get()
        self.ent.delete(0, END)

        if self.index_mode==0: #jika mode chat/text
            if ent_user!='':
                self.bsk_frame =ctk.CTkFrame(self.chatFrame,fg_color='transparent')
                self.bsk_frame.grid(row=len(self.list_frames),column=0,sticky='e')

                self.bsk_frame.grid_columnconfigure((0,1), weight=0)
                self.bsk_frame.grid_rowconfigure(0, weight=1)

                self.ch = ctk.CTkLabel(self.bsk_frame, text=self.my_name[0],font=('Helvetica',20,'bold'),height=30,width=30,fg_color='#037562',text_color='white',corner_radius=5)
                self.ch.grid(row=0,column=1,padx=10,pady=10)

                self.frame_text = ctk.CTkFrame(self.bsk_frame,corner_radius=15,height=30,fg_color='white')
                self.frame_text.grid(row=0,column=0)

                self.lbl_text=ctk.CTkLabel(self.frame_text, text=ent_user,font=('Helvetica',14)) #settingan kirim pesan
                self.lbl_text.grid(row=0,column=0,padx=10,pady=5,sticky='w')

                self.list_frames.append(self.bsk_frame)

                self.lower_frame = ctk.CTkFrame(self.frame_text,fg_color='transparent',corner_radius=20)
                self.lower_frame.grid(row=1,column=0,pady=2,padx=7,sticky='nswe')

                self.lower_frame.grid_rowconfigure(0, weight=0)

                self.lower_frame.grid_columnconfigure(0, weight=0)

                self.lower_frame.grid_columnconfigure(1, weight=1)

                timeNow = datetime.datetime.now()
                hour = timeNow.hour
                AM_PM = ' AM'
                if hour>=12:
                    AM_PM = ' PM'
                    if hour>12:
                        hour-=12
                hour = str(hour)
                minute = str(timeNow.minute)
                if len(hour)==1:
                    hour='0'+hour
                if len(minute)==1:
                    minute='0'+minute
                timeNowStr = hour + ':'+ minute + AM_PM

                self.lbl_time = ctk.CTkLabel(self.lower_frame,text=timeNowStr,font=('Helvetica',11))
                self.lbl_time.grid(row=0,column=1,sticky='w',padx=5)

                self.lbl_seen = ctk.CTkLabel(self.lower_frame,text='.',text_color='red')
                self.lbl_seen.grid(row=0,column=0)

                self.list_labels_info[self.index_chat][0].configure(text=ent_user)
                self.list_labels_info[self.index_chat][1].configure(text=timeNowStr)

                self.list_chat[self.index_chat].append({'M':ent_user,'R':False,'seen':False,'time':timeNowStr})

            else:
                pass #mau dibuat gambar nanti
        elif self.index_mode==1: #jika mode gambar
            #stop
            pass #mau dibuat gambar nanti

    def time_format(self,sec): # jika 70
        minutes = str(int(sec/60)) #jadi 01
        seconds = str(sec%60) #jadi 10
        if(len(minutes)==1):
            minutes='0'+minutes
        if(len(seconds)==1):
            seconds='0'+seconds

        return minutes+':'+seconds

    #Fungsi untuk mengambil data pesan
    def get_chats_Net(self):
        self.my_name = "Nohiro"
        self.list_persons=[
            {
                "name":'Richky Sachet',
                'time':'8:26 PM'
            },
            {
                "name":'Widi Stang Seher',
                'time':'02:00 AM'
            }
        ]
        self.list_chat=[
            [{'H':'Bang, aku sebenarnya suka sama elisa, tapi jgn ksih tau sp2','R':False, 'time':'8:26 PM','seen':True},
             {'M':'Aman bangg','R':False, 'time':'8:27 PM','seen':True},
             {'H':'pas matkul jarkom, aku mau confess ke dia','R':False, 'time':'8:29 PM','seen':True},
             {'M':'anjayy goodluck bang','R':False, 'time':'8:29 PM','seen':True},
             {'H':r'C:\Users\AU\Desktop\2024-5-28-15-10-45.wav','R':'True', 'time':'8:35 PM','seen':True}],

            [{'H':'Bang tolong aku diculik ambatron','R':False, 'time':'2:21 AM','seen':True},
             {'M':'dimana bang? biar ku telpon rusdi','R':False, 'time':'2:22 AM','seen':True},
             {'H':'di TA 10.5 bang, cepat bang tolong aku','R':False, 'time':'2:26 AM','seen':True},
             {'M':'iya iya sabar bang, rusdi lagi otw','R':False, 'time':'2:31 AM','seen':True}]
        ] # 'R':False disini berarti ini bukan record(rekaman suara), ini dibuat gini biar bisa kirim pesan suara

    #Fungsi untuk menampilkan orang yang ingin dichat (bagian kiri)
    def load_chats(self,ListPersons):
        for i in range(len(ListPersons)):
            info = list(self.list_chat[i][-1].values())[0]
            if list(self.list_chat[i][-1].values())[1]:
                info='Gambar' #mau dibuat gambar

            self.basicFrame = ctk.CTkFrame(self.leftFrame,fg_color='transparent',height=100,corner_radius=0)
            self.basicFrame.grid(row=i,column=0,sticky='nswe',pady=5)
            self.basicFrame.bind('<Button-1>',lambda e,a=i,chat=self.list_chat[i] :self.init_chat(e,a,chat))

            self.basicFrame.grid_rowconfigure(0, weight=1)
            self.basicFrame.grid_columnconfigure(0, weight=0)
            self.basicFrame.grid_columnconfigure(1, weight=1)

            self.lbl_ch = ctk.CTkLabel(self.basicFrame, text=ListPersons[i]['name'][0],font=('Helvetica',20,'bold',),height=40,width=40,fg_color='#25D366',text_color='white',corner_radius=10)
            self.lbl_ch.grid(row=0,column=0,padx=10,pady=10)
            self.lbl_ch.bind('<Button-1>',lambda e,a=i,chat=self.list_chat[i] :self.init_chat(e,a,chat))


            self.frameInfo = ctk.CTkFrame(self.basicFrame,fg_color='transparent',corner_radius=0)
            self.frameInfo.grid(row=0,column=1,sticky='nswe')

            # Koding saat pesan (kiri) di klik, akan menghasilkan index, lalu pesan dimunculkan tergantung index yang didapat
            #contoh, pencet urutan pertama itu index 0, nah si program ini nanti ambil data pesan index 0, lalu ditampilin
            self.frameInfo.bind('<Button-1>',lambda e,a=i,chat=self.list_chat[i] :self.init_chat(e,a,chat))

            self.frameInfo.grid_columnconfigure(0, weight=1)
            self.frameInfo.grid_rowconfigure((1,2,3), weight=0)
            self.frameInfo.grid_rowconfigure((0,4), weight=1)

            self.lbl_name=ctk.CTkLabel(self.frameInfo, text=ListPersons[i]['name'],font=('Helvetica',18,'bold'),height=5)
            self.lbl_name.grid(row=1,column=0,sticky='w')
            self.lbl_name.bind('<Button-1>',lambda e,a=i,chat=self.list_chat[i] :self.init_chat(e,a,chat))

            self.lbl_Info=ctk.CTkLabel(self.frameInfo, text=info,font=('Helvetica',14),height=5)
            self.lbl_Info.grid(row=2,column=0,sticky='w')
            self.lbl_Info.bind('<Button-1>',lambda e,a=i,chat=self.list_chat[i] :self.init_chat(e,a,chat))

            self.lbl_time=ctk.CTkLabel(self.frameInfo, text=ListPersons[i]['time'],font=('Helvetica',14),height=5)
            self.lbl_time.grid(row=3,column=0,sticky='w')
            self.lbl_time.bind('<Button-1>',lambda e,a=i,chat=self.list_chat[i] :self.init_chat(e,a,chat))

            self.list_labels_info.append([self.lbl_Info,self.lbl_time])

            self.lbl_divider = ctk.CTkFrame(self.basicFrame,fg_color='#e9edef',height=2)
            self.lbl_divider.grid(row=1,column=0,columnspan=2,sticky='nswe',pady=5,padx=5)

    #fungsi untuk menampilkan isi chat (bagian kanan)
    def init_chat(self,e,index,list_chat):
        if self.index_chat==-1 and self.index_chat!=index: #ini agar saat buka app tampilannya kosong
            self.ent = ctk.CTkEntry(self.footerFrame, placeholder_text='Type a message')
            self.ent.grid(row=0,column=0,sticky='nswe',padx=5,pady=10)

            self.bt_send = ctk.CTkButton(self.footerFrame, text='Send/Rec', font=('Helvetica',18),fg_color="#25D366",command=self.bt_send_com,hover_color='#1DA851')
            self.bt_send.grid(row=0,column=1,padx=5,pady=10)


        if self.index_chat!=index: #Ini agar tidak ngeload berulang pas pencet chat(kiri) yg sama
            self.index_chat = index

            self.ch = ctk.CTkLabel(self.headerFrame, text=self.list_persons[index]['name'][0],font=('Helvetica',20,'bold'),height=30,width=30,fg_color='#25D366',text_color='white',corner_radius=5)
            self.ch.grid(row=0,column=0,padx=10,pady=10)

            self.lbl_text=ctk.CTkLabel(self.headerFrame, text=self.list_persons[index]['name'],font=('Helvetica',16,'bold'))
            self.lbl_text.grid(row=0,column=1,pady=5,sticky='w')

            for i in range(len(self.list_frames)):
                self.list_frames[i].grid_forget()

            self.list_frames=[]
            self.list_rec={}

            for i in range(len(list_chat)):
                stick='e'
                sticky_time='w'
                row_pos=1
                ch=self.my_name[0]
                color='#037562'
                if list(list_chat[i].keys())[0]=='H':
                    sticky_time='e'
                    stick='w'
                    row_pos=0
                    ch = self.list_persons[index]['name'][0]
                    color='#25D366'
                
                self.bsk_frame =ctk.CTkFrame(self.chatFrame,fg_color='transparent')
                self.bsk_frame.grid(row=i,column=0,sticky=stick)

                self.bsk_frame.grid_columnconfigure((0,1), weight=0)
                self.bsk_frame.grid_rowconfigure(0, weight=1)

                self.ch = ctk.CTkLabel(self.bsk_frame, text=ch,font=('Helvetica',20,'bold'),height=30,width=30,fg_color=color,text_color='white',corner_radius=5)
                self.ch.grid(row=0,column=row_pos,padx=10,pady=10)

                self.frame_text = ctk.CTkFrame(self.bsk_frame,corner_radius=15,height=30,fg_color='white')
                self.frame_text.grid(row=0,column=1-row_pos)

                self.frame_text.grid_rowconfigure((0,1), weight=0)
                self.frame_text.grid_columnconfigure(0, weight=0)

                span=3
                if list_chat[i]['R']==False: #ini masih'R' record, nanti mau diubah jadi gambar
                    self.lbl_text=ctk.CTkLabel(self.frame_text, text=list(list_chat[i].values())[0],font=('Helvetica',14)) #settingan pesan yang tersimpan
                    self.lbl_text.grid(row=0,column=0,padx=10,pady=5,sticky='w')
                    span=1
                else:
                    pass
                
                self.lower_frame = ctk.CTkFrame(self.frame_text,fg_color='transparent',corner_radius=20)
                self.lower_frame.grid(row=1,column=0,columnspan=span,pady=2,padx=7,sticky='nswe')

                self.lower_frame.grid_rowconfigure(0, weight=0)

                self.lower_frame.grid_columnconfigure(0, weight=0)

                self.lower_frame.grid_columnconfigure(1, weight=1)

                self.lbl_time = ctk.CTkLabel(self.lower_frame,text=self.list_chat[self.index_chat][i]['time'],font=('Helvetica',11),text_color='gray')
                self.lbl_time.grid(row=0,column=1,sticky=sticky_time,padx=5)

                if list(list_chat[i].keys())[0]=='M':
                    color_seen='red'
                    if list_chat[1]['seen']:
                        color_seen = '#25D366'
                    self.lbl_seen = ctk.CTkLabel(self.lower_frame,text='.',text_color=color_seen)
                    self.lbl_seen.grid(row=0,column=0)

                self.list_frames.append(self.bsk_frame)

if __name__=='__main__':
    app=App()
    app.mainloop()
