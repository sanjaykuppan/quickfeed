from tkinter import *
import pymongo
from tkinter import messagebox
import ace
from ace import AutocompleteEntry
import json

def adduser():
    try:    
        dbname="quickfeed"
        colname="userdetail"
        smelist=[]
        managerlist=[]
        clusterlist=[]
        idlist=[]
        with open('dbdata.json', 'r') as file:
            data=file.read()
        mongoclient=json.loads(data)
        connectlink=mongoclient["mongoclient"]
        client=pymongo.MongoClient(connectlink)
        db=client.quickfeed
        statcol=db.staticdetail
        usercol=db.userdetail
        smelist=statcol.distinct("sme")
        managerlist=statcol.distinct("manager")
        clusterlist=statcol.distinct("cluster")
        idlist=usercol.distinct("id")
        #print(smelist,managerlist,clusterlist)
        totcol=db.list_collection_names()
        if colname in totcol and len(smelist) != 0 and len(managerlist) !=0 and len(clusterlist) !=0:
            addwin=Tk()
            addwin.title("Add user")
            addwin.geometry("400x400")
            frametop=Frame(addwin)
            framemiddle=Frame(addwin)
            framebottom=Frame(addwin)
            idv=StringVar() #email id value
            namv=StringVar() #name value
            #print(len(idv.get()),len(namv.get()))
            LT=Label(frametop,text="Add User")
            LT.pack(side='top',pady=5)
            L1=Label(framemiddle,text="Email ID")
            L1.grid(row=0,column=0,pady=5)
            E1=Entry(framemiddle,text="Userid",width=40,textvariable=idv)
            E1.grid(row=0,column=1,pady=5)
            L2=Label(framemiddle,text="Name")
            L2.grid(row=1,column=0,pady=5)
            E2=Entry(framemiddle,text="name",width=40,textvariable=namv)
            E2.grid(row=1,column=1,pady=5)
            L3=Label(framemiddle,text="sme")
            L3.grid(row=2,column=0,pady=10)
            E3=AutocompleteEntry(smelist,framemiddle)
            E3.grid(row=2,column=1,pady=10)
            L4=Label(framemiddle,text="manager")
            L4.grid(row=3,column=0,pady=10)
            E4=AutocompleteEntry(managerlist,framemiddle)
            E4.grid(row=3,column=1,pady=10)
            L5=Label(framemiddle,text="cluster")
            L5.grid(row=4,column=0,pady=40)
            E5=AutocompleteEntry(clusterlist,framemiddle)
            E5.grid(row=4,column=1,pady=40)
            def add():
                if idv.get() in idlist:
                    messagebox.showinfo(parent=addwin,title="Error",message="User id already exists!!")
                if len(idv.get()) !=0 and len(namv.get()) != 0 and E3.get() in smelist and E4.get() in managerlist and E5.get() in clusterlist and idv.get() not in idlist:    
                    data={"id":idv.get(),"name":namv.get(),"sme":E3.get(),"manager":E4.get(),"cluster":E5.get()}
                    usercol.insert_one(data)
                    #print(data,type(data),len(idv.get()),len(namv.get()))
                    idv.set('')
                    namv.set('')
                    #print("after",len(idv.get()))
                    messagebox.showinfo(parent=addwin,title="Success",message="Add user successful!!")
                    return
                else :
                    messagebox.showinfo(parent=addwin,title="Error",message="Data Missing or Data mismatch!! Please fill all details correctly and select only from dropdown menu for drop down list")
            def exitbox():
                client.close()
                addwin.destroy()
                return
            B1=Button(framebottom,text="Add",command=add)
            B1.pack(side='left',padx=5)
            BE=Button(framebottom,text="Exit",command=exitbox)
            BE.pack(side='right',padx=5)
            frametop.pack(side='top')
            framemiddle.pack(side='top')
            framebottom.pack(side='top',pady=5)
            addwin.mainloop()
    except:
        messagebox.showinfo(title="Error",message="possible cause :No internet connection!!")
        return

if __name__ == "__main__":
    app=adduser()




    