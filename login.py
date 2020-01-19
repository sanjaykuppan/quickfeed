from tkinter import *
from tkinter import messagebox
import pymongo
import questionfeedback as qf
import contributionfeedback as cform
import json

def login():
    try:
        with open('dbdata.json', 'r') as file:
            data=file.read()
        mongoclient=json.loads(data)
        connectlink=mongoclient["mongoclient"]
        client=pymongo.MongoClient(connectlink)
        db=client.quickfeed
        statcol=db.staticdetail
        usercol=db.userdetail
        idlist=[]
        idlist=usercol.distinct("id")
        #print(idlist)
        box=Tk()
        box.title("QuickFeed")
        #box.state("zoomed")
        frametop=Frame(box)
        framebottom=Frame(box)
        L1=Label(frametop,text="Email id")
        L1.grid(row=0,column=0,padx=10,pady=20)
        E1=Entry(frametop,text="id",width=40)
        E1.grid(row=0,column=1,padx=10,pady=20)
        def enter():
            if E1.get() in idlist:
                user=E1.get()
                frametop.destroy()
                framebottom.destroy()
                framechoice=Frame(box)
                def qfeed():
                    stcol=db.surveytakenlist
                    tlist=stcol.distinct("id",{"st":"qf"})
                    if user not in tlist:
                        qf.questionform(user)
                    else:
                        messagebox.showinfo(parent=box,title="Not allowed",message="Already taken survey!! Please try contribution feedback")
                    return
                def cf():
                    stcol=db.surveytakenlist
                    tlist=stcol.distinct("id",{"st":"cf"})
                    if user not in tlist:
                        cform.contributionform(user)
                    else:
                        messagebox.showinfo(parent=box,title="Not allowed",message="Already taken survey!! Please try Question feedback")
                    return
                    return
                ud=Label(framechoice,text=user)
                ud.pack(side='top')
                BS1=Button(framechoice,text="Question feedback",command=qfeed)
                BS1.pack(side='top',padx=10,pady=10)
                BS2=Button(framechoice,text="Contribution feedback",command=cf)
                BS2.pack(side='top',padx=10,pady=10)
                framechoice.pack(side='top')
            else:
                messagebox.showinfo(title="error",message="Id does not exists!")
            return
        def ex():
            client.close()
            box.destroy()
        B1=Button(framebottom,text="Login",command=enter)
        B1.grid(row=0,column=0,padx=10,pady=20)
        B2=Button(framebottom,text="exit",command=ex)
        B2.grid(row=0,column=1,padx=10,pady=20)
        frametop.pack(side='top')
        framebottom.pack(side='top')
        box.mainloop()
    except:
        messagebox.showinfo(title="Error",message="possible cause :No internet connection!!")
        return

if __name__ == "__main__":
    login()