from tkinter import *
from tkinter import messagebox
import pymongo
import sys
import json

def questionform(id):
    try:
        with open('dbdata.json', 'r') as file:
            data=file.read()
        mongoclient=json.loads(data)
        connectlink=mongoclient["mongoclient"]
        client=pymongo.MongoClient(connectlink)
        db=client.quickfeed
        qcol=db.questions
        qidlist=[]
        qlist=[]
        l=[]
        a=[]
        lq=[]
        qidlist=qcol.distinct("qid")
        qlist=qcol.distinct("question")
        qwin=Toplevel()
        qwin.state("zoomed")
        qwin.grab_set()
        frametop=Frame(qwin)
        framebottom=Frame(qwin)
        qwin.title("Feedback questions")
        j=0
        for i in range(0,10):
            li=Label(frametop,text=qidlist[i])
            li.grid(row=j,column=0,pady=10)
            l.append(li)
            lqi=Label(frametop,text=qlist[i])
            lqi.grid(row=j,column=1,pady=10)
            lq.append(lqi)
            ai=Entry(frametop,width=70) #entry widget
            ai.grid(row=j+1,column=1,pady=5)
            a.append(ai)
            j+=2
        frametop.pack(side='top')
        framebottom.pack(side='bottom')
        def sub():
            ans=[]
            sicol=db.surveyinfo
            anscol=db.answer
            stcol=db.surveytakenlist
            surveydet=str(sicol.distinct("surveydetail")[0])
            #print(surveydet,type(surveydet))
            i=1
            for an in a:
                anscol.insert_one({"answer":an.get(),"surveydetail":surveydet,"qid":i})
                #data={"answer":an.get(),"surveydetail":surveydet,"qid":i}
                #print(data)
                i+=1
            stcol.insert_one({"id":id,"surveydetail":surveydet,"st":"qf"})
            messagebox.showinfo(parent=qwin,title="Success",message="feedback registered successfully")
            client.close()
            frametop.destroy()
            framebottom.destroy()
            qwin.destroy()
            return
        def ex():
            client.close()
            frametop.destroy()
            framebottom.destroy()
            qwin.destroy()
            return
        b1=Button(framebottom,text="Submit",command=sub)
        b1.pack(side='left',padx=50,pady=10)
        b2=Button(framebottom,text='Exit',command=ex)
        b2.pack(side='right',padx=50,pady=10)
        qwin.mainloop()
    except :
        messagebox.showinfo(title="Error",message="possible cause :No internet connection!!")
        return

#questionform()
if __name__ == "__main__":
    id='sanjayk8@in.ibm.com'
    app=questionform(id)