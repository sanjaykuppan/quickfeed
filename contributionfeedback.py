from tkinter import *
from tkinter import messagebox
import pymongo
import json

def contributionform(id):
    with open('dbdata.json', 'r') as file:
        data=file.read()
    mongoclient=json.loads(data)
    connectlink=mongoclient["mongoclient"]
    client=pymongo.MongoClient(connectlink)
    db=client.quickfeed
    stcol=db.surveytakenlist
    sicol=db.surveyinfo
    surveydet=str(sicol.distinct("surveydetail")[0])
    ucol=db.userdetail
    ufcol=db.userfeedback
    clust=ucol.distinct("cluster",{"id":id})[0]
    #print(clust)
    clist=ucol.distinct("id",{"cluster":clust})
    clist.remove(id)
    cwin=Toplevel()
    #cwin.state("zoomed")
    cwin.grab_set()
    frametop=Frame(cwin)
    framebottom=Frame(cwin)
    et=StringVar()
    ec=StringVar()
    ee=StringVar()
    et.set(clist[0])
    def block(ins):
        if ins=='1' or ins=='0':
            return False
        elif ins=='-1':
            return True
    LT=Label(frametop,text="Colleague")
    LT.grid(row=0,column=0)
    ET=Entry(frametop,textvariable=et,validate='key')
    ET['validatecommand']=(ET.register(block),'%d')
    ET.grid(row=0,column=1)
    L1=Label(frametop,text="Cotnributions")
    L1.grid(row=1,column=0)
    E1=Entry(frametop,textvariable=ec,width=60)
    E1.grid(row=1,column=1)
    L2=Label(frametop,text="Expectations")
    L2.grid(row=2,column=0)
    E2=Entry(frametop,textvariable=ee,width=60)
    E2.grid(row=2,column=1)
    frametop.pack(side='top')
    def nex():
        clist.pop(0)
        data={"id":et.get(),"contribution":ec.get(),"expectation":ee.get()}
        ufcol.insert_one(data)
        if len(clist) != 0 :
            et.set(clist[0])
            ec.set('')
            ee.set('')
        else:
            
            stcol.insert_one({"id":id,"surveydetail":surveydet,"st":"cf"})
            messagebox.showinfo(parent=cwin,title="complete",message="Survey complete !")   
            cwin.destroy()
        return
    B1=Button(framebottom,text="continue to next person",command=nex)
    B1.pack(side='right',pady=20,padx=50)
    def ex():
        cwin.destroy()
    B2=Button(framebottom,text="Exit",command=ex)
    B2.pack(side='bottom',pady=20)
    framebottom.pack(side='bottom')
    cwin.mainloop()
