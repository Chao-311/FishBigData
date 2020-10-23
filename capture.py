# -*- coding=utf-8 -*-
# import re
from tkinter import *
from tkinter import messagebox	#消息窗口
from tkinter import filedialog	#文件选择框
import os 						#打开notebook
import tkinter.ttk as ttk
import requests
from pyquery import PyQuery as pq
import time
from lxml import etree
from retrying import retry
from bs4 import BeautifulSoup
import lxml
# 样式定义
fontStyle0="SimHei 36 bold"		#总标题的文字样式
fontStyle1="KaiTi 12"			#Tips中文字的样式
fontStyle2="SimHei 20 bold"   	#所有的单独提示文字
fontStyle3="KaiTi 16 bold"		#按钮的文字样式
fontLabFrame="SimHei 14 bold"	#LabelFrame头的文字样式
pady1=20						#定义标签之间的竖向距离
padx1=10						#定义标签之间的横向距离
btnWidth=15						#定义btn的宽
btnWidth1=10
btnHei=2
padx2=5
pady2=5
padx3=2
pady3=2
etyWidth=55
etyHeight=10
btnHeight=1

# 定义全局变量
SPNMstr=""
MSGstr=""
fileNameSPNM=""
fileNameMsg=""
keyList=[]
ifFile1=0
ifFile2=0
def helpMsg():
	messagebox.showinfo("帮助","通过点击按钮和输入内容进行操作，详情请参见《全球鱼类大数据爬取与处理(1.0版)软件说明书》")
def aboutMsg():
	messagebox.showinfo("关于","全球鱼类大数据爬取与处理\n版本：V1.0\n制作人：胡嘉欣\n邮箱：937026873@qq.com")
# 上传物种名称文件三个button的点击事件
def readfileSPNM():							#按行读取speciesName文件
	global fileNameSPNM						#进行声明后才可以修改全局变量
	fileNameSPNM=str(filedialog.askopenfilename())
	print(fileNameSPNM)
	lab1_1.configure(text=fileNameSPNM)

def subfileSPNM():
	global SPNMstr
	if fileNameSPNM=="":
		messagebox.showwarning("重要提示","请选择文件！")
	else:
		f1 = open(fileNameSPNM,"r")
		SPNMstr = f1.read()				
		f1.close()
		lab1_1.configure(bg="LightBlue")
		# print(Gstr)

def clearfileSPNM():
	global fileNameSPNM						#进行声明后才可以修改全局变量
	global SPNMstr
	fileNameSPNM=""
	SPNMstr=""
	lab1_1.configure(text=fileNameSPNM)
	lab1_1.configure(bg="white")

# 上传物种信息文件三个button的点击事件
def readfileMsg():							#按行读取GeneGroup文件
	global fileNameMsg						#进行声明后才可以修改全局变量
	fileNameMsg=str(filedialog.askopenfilename())
	print(fileNameMsg)
	lab2_1.configure(text=fileNameMsg)

def subfileMsg():
	global MSGstr
	if fileNameMsg=="":
		messagebox.showwarning("重要提示","请选择文件！")
	else:
		f2 = open(fileNameMsg,"r")
		MSGstr = f2.readlines()				
		f2.close()
		lab2_1.configure(bg="LightBlue")
		# print(Mstr)
def clearfileMsg():
	global fileNameMsg						#进行声明后才可以修改全局变量
	global MSGstr
	fileNameMsg=""
	MSGstr=""
	lab2_1.configure(text=fileNameMsg)
	lab2_1.configure(bg="white")


def subMain1():
	global fileNameSPNM
	global ifFile1
	if SPNMstr=="":

		messagebox.showwarning("重要提示","请选择文件！")
	else:
		url = "http://researcharchive.calacademy.org/research/ichthyology/catalog/fishcatmain.asp"   #这个是固定的
		List = SPNMstr.split("\n")
		a=len(List)
		listbx.insert(END,"爬取进行中......")
		index.update()
		result=[]
		i=0
		while i<a:
				file1 = List[i]
				data = {"tbl":"Species",
						"contains":file1,
						"Submit": "Search"}


				@retry(stop_max_attempt_number=3)
				def _parse_url(url):
						req = requests.post(url, data,timeout=30)  # 超时的时候回报错并重试
						assert req.status_code == 200  # 状态码不是200，也会报错并充实
						return
				def parse_url(url):
						try:  # 进行异常捕获
								 req = _parse_url(url)
						except Exception as e:
								messagebox.showwarning("异常捕获",e)
								req = None

						return req



				req = requests.post(url, data, timeout=30)
				doc = pq(req.text)
				need = doc(".result").text()
				result.append(need + "\n")
				
				time.sleep(20)
				f = open('nameresult.txt', 'w',encoding="utf-8")
				f.writelines(result)
				f.close()
				ifFile1=1
				i = i+1
				Journal=file1+"  已爬取完成！"
				print(file1+"	complete!")
				listbx.insert(END,str(i)+". "+Journal)
				index.update()
		listbx.insert(END,"爬取完成全部文件！")
		index.update()

def viewResult1():
	if ifFile1==1:
		# os.system('gedit OutputResult.txt')		#Ubuntu下激活本条语句
		os.system('notepad nameresult.txt')	#windows下激活本条语句
	else:
		messagebox.showwarning("重要提示","尚未生成结果文件！")



def subMain2():
	global fileNameMsg
	global ifFile2
	if MSGstr=="":
		messagebox.showwarning("重要提示","请选择文件！")
	else:
		optnList=[]
		if var1.get()==1:
			optnSingle="insdseq_locus"			#序列号
			optnList.append(optnSingle)
		if var2.get()==1:
			optnSingle="insdseq_organism"		#物种
			optnList.append(optnSingle)
		if var3.get()==1:
			optnSingle="insdreference_title"	#文献名
			optnList.append(optnSingle)
		if var4.get()==1:
			optnSingle="insdreference_journal"	#期刊
			optnList.append(optnSingle)
		if var5.get()==1:
			optnSingle="insdauthor"				#作者
			optnList.append(optnSingle)
		if var6.get()==1:
			optnSingle="insdseq_sequence"		#序列
			optnList.append(optnSingle)
		if optnList==[]:
			messagebox.showwarning("重要提示","请至少勾选一项需要提取的信息！")
		else:
			i=0
			file = open(fileNameMsg,'rb')
			html = file.read()
			result = []
			bs = BeautifulSoup(html,"lxml")
			need = bs.find_all(name = "insdseq")
			usefulMsg=""
			for use in need:
				for optn in optnList:
					usefulMsg = usefulMsg+str(use.find_all(optn))  #usefulMsg用来拼接筛选后所有需要输出的基因部分
					# print(optn)
					# print(str(use.find_all(optn)))
					# print(usefulMsg)
					result.append(usefulMsg)
				f = open('resultSelect.txt', 'w')
				f.writelines(result)
				f.close()
				print(i)
				i+=1
				print(optn)
			print(optnList)
			messagebox.showwarning("重要提示","已顺利提取您想要的信息，输入到resultSelect.txt文件中！")
			ifFile2=1
			
def viewResult2():
	if ifFile2==1:
		# os.system('gedit OutputResult.txt')		#Ubuntu下激活本条语句
		os.system('notepad resultSelect.txt')	#windows下激活本条语句
	else:
		messagebox.showwarning("重要提示","尚未生成结果文件！")
import tkinter
# 基本信息
index=Tk()
index.title("全球鱼类大数据爬取与处理")
index.iconbitmap("favicon.ico")
index.geometry("900x500+100+100")
# title
titlePic=PhotoImage(file="LOGO.gif",width=120,height=90)
labTitle1=Label(index,text=" 全球鱼类大数据爬取与处理",image=titlePic,compound="left",
		font=fontStyle0)
labTitle1.grid(row=0,column=0,columnspan=2,sticky=W+E,pady=pady1,padx=padx1)
# noteBook
notebook=ttk.Notebook(index)
frame1=Frame()
frame2=Frame()
notebook.add(frame1,text="爬取物种基本信息")
notebook.add(frame2,text="物种关键信息提取")
notebook.grid(row=1,column=0,sticky=W+E,padx=padx1)

# notebook1中的上传文件
lbfm1=LabelFrame(frame1,text="上传存储物种名信息的文件",font=fontLabFrame)
lab1_1=Label(lbfm1,relief="sunken",bg="white",anchor="w",pady=pady2)
btn1_1=Button(lbfm1,text="选择目录",font=fontStyle3,width=btnWidth,command=readfileSPNM,
	bg="LightBlue",height=btnHeight,pady=pady2)
btn1_2=Button(lbfm1,text="清除",font=fontStyle3,width=btnWidth,command=clearfileSPNM,
	bg="DarkOrange",fg="white",pady=pady2)
btn1_3=Button(lbfm1,text="确定",font=fontStyle3,width=btnWidth,command=subfileSPNM,
	bg="DarkGreen",fg="white",height=btnHeight,pady=pady2)
lab1_1.grid(row=0,column=0,columnspan=3,sticky=W+E,padx=padx2,pady=pady2)
btn1_1.grid(row=1,column=0,padx=padx2,pady=pady2)
btn1_2.grid(row=1,column=1,padx=padx2,pady=pady2)
btn1_3.grid(row=1,column=2,padx=padx2,pady=pady2)
lbfm1.grid(row=0,column=0,sticky=W+E,padx=padx3,pady=pady3)

# notebook1中的listbox
lbfmLbx=LabelFrame(frame1,text="爬取日志",font=fontLabFrame)
scrollbar=Scrollbar(lbfmLbx)
scrollbar.grid(row=0,column=1,sticky=N+S+E+W,padx=padx3,pady=pady3)
listbx=Listbox(lbfmLbx,width=81,yscrollcommand=scrollbar.set)
# for i in range(50):
# 	listbx.insert(END,"LINE"+str(i))
listbx.grid(row=0,column=0,sticky=W+E,padx=padx3,pady=pady3)
lbfmLbx.grid(row=1,column=0,sticky=W+E,padx=padx3,pady=pady3)
scrollbar.config(command=listbx.yview)

# notebook1中的button组
buttonFrm1=Frame(frame1)
btnHelp1=Button(buttonFrm1,text="帮助",font=fontStyle3,width=btnWidth1,command=helpMsg,
	height=btnHei,anchor="c",bg="purple",fg="white")
btnAbout1=Button(buttonFrm1,text="关于",font=fontStyle3,width=btnWidth1,command=aboutMsg,
	height=btnHei,anchor="c",bg="purple",fg="white")
btnExit1=Button(buttonFrm1,text="退出",font=fontStyle3,command=index.destroy,width=btnWidth1,
	height=btnHei,anchor="c",bg="Crimson",fg="white")
btnSub1=Button(buttonFrm1,text="提交",font=fontStyle3,width=btnWidth,height=btnHei,command=subMain1,
	bg="DarkGreen",fg="white")
btnView1=Button(buttonFrm1,text="查看结果",font=fontStyle3,width=btnWidth,height=btnHei,command=viewResult1,
	bg="DarkBlue",fg="white")
btnExit1.grid(row=1,column=1,sticky=W+E,pady=pady2,padx=padx1)
btnHelp1.grid(row=2,column=1,sticky=W+E,pady=pady2,padx=padx1)
btnAbout1.grid(row=3,column=1,sticky=W+E,pady=pady2,padx=padx1)
btnSub1.grid(row=4,column=1,padx=padx1,pady=pady2,sticky=S)
btnView1.grid(row=5,column=1,padx=padx1,pady=pady2)
buttonFrm1.grid(row=0,column=1,rowspan=2,stick=N+S,padx=padx1,pady=0)

# notebook2中的上传文件
lbfm2=LabelFrame(frame2,text="上传物种基本信息文件",font=fontLabFrame)
lab2_1=Label(lbfm2,relief="sunken",bg="white",anchor="w",pady=pady2)
btn2_1=Button(lbfm2,text="选择目录",font=fontStyle3,width=btnWidth,command=readfileMsg,
	bg="LightBlue",height=btnHeight,pady=pady2)
btn2_2=Button(lbfm2,text="清除",font=fontStyle3,width=btnWidth,command=clearfileMsg,
	bg="DarkOrange",fg="white",height=btnHeight,pady=pady2)
btn2_3=Button(lbfm2,text="确定",font=fontStyle3,width=btnWidth,command=subfileMsg,
	bg="DarkGreen",fg="white",height=btnHeight,pady=pady2)
lab2_1.grid(row=0,column=0,columnspan=3,sticky=W+E,padx=padx2,pady=pady2)
btn2_1.grid(row=1,column=0,padx=padx2,pady=pady2)
btn2_2.grid(row=1,column=1,padx=padx2,pady=pady2)
btn2_3.grid(row=1,column=2,padx=padx2,pady=pady2)
lbfm2.grid(row=0,column=0,sticky=W+E,padx=padx3,pady=pady3)
# notebook2中的复选框部分
lbfmCheck=LabelFrame(frame2,text="选择需要提取的信息",font=fontLabFrame)
var1=IntVar()
var2=IntVar()
var3=IntVar()
var4=IntVar()
var5=IntVar()
var6=IntVar()
cbtn1=Checkbutton(lbfmCheck,text="序列号",variable=var1,offvalue=0,onvalue=1,font=fontStyle1)
cbtn2=Checkbutton(lbfmCheck,text="物种名称",variable=var2,offvalue=0,onvalue=1,font=fontStyle1)
cbtn3=Checkbutton(lbfmCheck,text="文献名称",variable=var3,offvalue=0,onvalue=1,font=fontStyle1)
cbtn4=Checkbutton(lbfmCheck,text="期刊名称",variable=var4,offvalue=0,onvalue=1,font=fontStyle1)
cbtn5=Checkbutton(lbfmCheck,text="作者",variable=var5,offvalue=0,onvalue=1,font=fontStyle1)
cbtn6=Checkbutton(lbfmCheck,text="序列",variable=var6,offvalue=0,onvalue=1,font=fontStyle1)
cbtn1.grid(row=0,column=0,sticky=W+E,padx=padx1)
cbtn2.grid(row=0,column=1,sticky=W+E,padx=padx1)
cbtn3.grid(row=0,column=2,sticky=W+E,padx=padx1)
cbtn4.grid(row=0,column=3,sticky=W+E,padx=padx1)
cbtn5.grid(row=0,column=4,sticky=W+E,padx=padx1)
cbtn6.grid(row=0,column=5,sticky=W+E,padx=padx1)
lbfmCheck.grid(row=1,column=0,sticky=W+E,padx=padx3)
# notebook2中的help文字部分
lbhelp=Label(frame2,font=fontStyle1,relief="sunken",bg="white",
	text="请按照提示内容进行操作\n"
	"1、选择上传所需文件，点击“确定”按钮\n"
	"2、文件选择错误，点击“清除”按钮后重新上传\n"
	"3、文件上传无误，点击“提交”按钮，程序自动运行\n"
	"4、点击“查看结果”按钮可以查看整理好的结果文件\n"
	"5、关于本软件的详细介绍请查看《全球鱼类大数据爬取与处理(1.0版)软件说明书》\n"
	"到此行结束",
	anchor="nw",justify="left",wraplength=600)
lbhelp.grid(row=2,column=0,sticky=W+E,padx=padx3)
# notebook2中的button组
buttonFrm2=Frame(frame2)
btnHelp2=Button(buttonFrm2,text="帮助",font=fontStyle3,width=btnWidth1,
	height=btnHei,anchor="c",bg="purple",fg="white")
btnAbout2=Button(buttonFrm2,text="关于",font=fontStyle3,width=btnWidth1,
	height=btnHei,anchor="c",bg="purple",fg="white")
btnExit2=Button(buttonFrm2,text="退出",font=fontStyle3,command=index.destroy,width=btnWidth1,
	height=btnHei,anchor="c",bg="Crimson",fg="white")
btnSub2=Button(buttonFrm2,text="提交",font=fontStyle3,width=btnWidth,height=btnHei,command=subMain2,
	bg="DarkGreen",fg="white")
btnView2=Button(buttonFrm2,text="查看结果",font=fontStyle3,width=btnWidth,height=btnHei,command=viewResult2,
	bg="DarkBlue",fg="white")
btnExit2.grid(row=1,column=1,sticky=W+E,pady=pady2,padx=padx1)
btnHelp2.grid(row=2,column=1,sticky=W+E,pady=pady2,padx=padx1)
btnAbout2.grid(row=3,column=1,sticky=W+E,pady=pady2,padx=padx1)
btnSub2.grid(row=4,column=1,padx=padx1,pady=pady2,sticky=S)
btnView2.grid(row=5,column=1,padx=padx1,pady=pady2)
buttonFrm2.grid(row=0,column=1,rowspan=3,stick=N+S,padx=padx1,pady=0)
index.mainloop()