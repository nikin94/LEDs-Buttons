import RPi.GPIO as GPIO
import time
import random
from gpiozero import LED
from gpiozero import Button as Button_gpio
from tkinter import *

leds = [LED(4),LED(15),LED(17),LED(22),LED(24),LED(6),LED(19),LED(20)]
buttons = [Button_gpio(3),Button_gpio(14),Button_gpio(18),Button_gpio(27),Button_gpio(23),Button_gpio(5),Button_gpio(13),Button_gpio(16)]
colors = ['red', 'orange', 'gold', 'green', 'cyan' ,'blue', 'violet']

###
#leds.reverse()
#buttons.reverse()
###

t = 5 #times to repeat
pause = 0.5
roundTo = 3
labelAttemptsArray = []
ovalClicks = []
ovals = []

root = Tk()

def init():
    root.title('Тренажёр для перемещений')
    root.geometry('400x240+0+0')
    root.attributes('-fullscreen',True)
    create_ovals(40,5)
    
    
def clearall(p=1):
    global labelAttemptsArray
    for i in leds:
        i.on()
        i.off()
    for i in labelAttemptsArray:
        i.grid_remove()
    labelAttemptsArray.clear()
    labelTotaltime2.config(text='0.000')
    labelRepeats2.config(text='0/'+str(t))
    labelFastest2.config(text='0.000')
    labelSlowest2.config(text='0.000')
    labelAverage2.config(text='0.000')
    for i in ovals:
        canvas.itemconfig(i, fill='')
    if p:
        print('\n'*50)
    unBindOvalClick()
    rb[1].select()
    
def go(arr=0):
    if mode.get()==1:
        return
    intro()
    clearall(0)
    root.update()
    global labelAttemptsArray
    count=1
    k=-1
    timer_sum=0 #total time
    times = []
    if not arr:
        backcount=int(t)
        while backcount!=0:
            i=random.randint(0,7)
            while i==k:
                i=random.randint(0,7)
            k=i
            timer1 = round(time.time(),roundTo)
            waitForPress(i)
            timer2 = round(time.time() - timer1,roundTo)
            timer_sum = round(timer_sum + timer2,roundTo)
            print(count,':',timer2)

            labelRepeats2.config(text=str(count)+'/'+str(t))
            labelTotaltime2.config(text=timer_sum)
#            printAttempt(count, timer2, statsRow)

            backcount=backcount-1
            count=count+1
            times.append(timer2)       
            root.update()
    else:
        backcount=len(arr)
        while backcount!=0:
            i=7-arr.pop(0)
            timer1 = round(time.time(),roundTo)
            waitForPress(i)
            timer2 = round(time.time() - timer1,roundTo)
            timer_sum = round(timer_sum + timer2,roundTo)
            print(count,':',timer2)

            labelRepeats2.config(text=str(count)+'/'+str(len(times)+1))
            labelTotaltime2.config(text=timer_sum)
#            printAttempt(count, timer2, statsRow+7)

            backcount=backcount-1
            count=count+1
            times.append(timer2)       
            root.update()

#    labelAttemptsArray[times.index(max(times))*2].config(bg='tomato')
#    labelAttemptsArray[times.index(max(times))*2+1].config(bg='tomato')

#    labelAttemptsArray[times.index(min(times))*2].config(bg='lime green')
#    labelAttemptsArray[times.index(min(times))*2+1].config(bg='lime green')

    labelFastest2.config(text=min(times))
    labelSlowest2.config(text=max(times))
    labelAverage2.config(text=round(timer_sum/(count-1),roundTo))
    
    print('Total time for',count-1,'repeats is: ',timer_sum)
    print('Fastest attempt:',times.index(min(times))+1,'-',min(times))
    print('Slowest attempt:',times.index(max(times))+1,'-',max(times))
    print('Average time:',round(timer_sum/(count-1),roundTo),'\n===============================')
    
def intro():
    t=0
    while t<3:
        for i in leds:
            i.on()
        time.sleep(0.3)
        for i in leds:
            i.off()
        time.sleep(0.3)
        t=t+1

def printAttempt(number, time, row_):
    row_=row_+len(labelAttemptsArray)
    labelAttemptsArray.append(Label(root, text=str(number)+') '))
    labelAttemptsArray[len(labelAttemptsArray)-1].grid(row=row_, column=0)
    labelAttemptsArray.append(Label(root, text=str(time), font='arial 11'))
    labelAttemptsArray[len(labelAttemptsArray)-1].grid(row=row_, column=1)
    return labelAttemptsArray

def create_ovals(d, step, i=0, k=0):
    while k<3:
        while i<3:
            if k == 1 and i == 1:
                i=i+1
            else:
                ovals.append(canvas.create_oval(step+i*(d+2*step),step+k*(d+2*step),step+d+i*(d+2*step),step+d+k*(d+2*step)))
                i=i+1
        k=k+1
        i=0
    ovals.reverse();
    #ovals reverse

def waitForPress(i):
    leds[i].on()
    canvas.itemconfig(ovals[len(ovals)-i-1], fill='yellow')
    root.update()
    buttons[i].wait_for_press()
    leds[i].off()
    canvas.itemconfig(ovals[len(ovals)-i-1], fill='')
    root.update()
    time.sleep(pause)

def ovalWaitForClick(event):
    clicked=event.widget.find_closest(event.x,event.y)[0]-1
    clicked_reverse=8-event.widget.find_closest(event.x,event.y)[0]
    if(mode.get()==0):  #random
        goButton.config(command=go)
        unBindOvalClick()
    elif(mode.get()==1):  #single
        goButton.config(command=go)
        canvas.unbind('<ButtonPress-1>')
        waitForPress(clicked)
        canvas.bind('<ButtonPress-1>', ovalWaitForClick)
    elif(mode.get()==2):  #path
        goButton.config(command= lambda: go(ovalClicks))
        colors.append(colors[0])
        canvas.itemconfigure(ovals[clicked_reverse], fill=colors.pop(0))
        ovalClicks.append(clicked_reverse)

def bindOvalClick():
    canvas.bind('<ButtonPress-1>', ovalWaitForClick)
    for i in ovals:
        canvas.itemconfig(i, fill='')
    
def unBindOvalClick():
    canvas.unbind('<ButtonPress-1>')
    for i in ovals:
        canvas.itemconfigure(i, fill='')
    global t, ovalClicks
#    t=entryRepeats.get()
    ovalClicks = []
    root.update()

goButton = Button(root, text="Пyск", font="arial 16", command=go, height = '1', width= '6')
goButton.grid(row=0,column=0)

clearallButton = Button(root, text='Сброс', command = clearall, height = '1', width= '5')
clearallButton.grid(row=0,column=1)

canvas = Canvas(root, width=150, height=150, bg='white')
canvas.grid(row=1,column=0, columnspan=2, rowspan=6)

labelSetMode = Label(root, text='Режим:')
#labelSetMode.grid(row=0,column=2, sticky=E)

labelSetTimes = Label(root, text='Число повторений: '+str(t))
labelSetTimes.grid(row=7, column=0, columnspan=2)

#labelEntryRepeats = Label(root, text='5', width=2, bd=1)
#labelEntryRepeats.grid(row=8, column=0, columnspan=2)

def entryRepeatsGet(sign=0):
    global t
    t = t + sign
    if t==0 :
        t=1
    labelSetTimes.config(text='Число повторений: '+str(t))
    root.focus()
    root.update()

entryRepeatsButtonMinus = Button(root, text='Меньше', command=lambda: entryRepeatsGet(-1))
entryRepeatsButtonMinus.grid(row=9, column=0)

entryRepeatsButtonPlus = Button(root, text='Больше', command=lambda: entryRepeatsGet(1))
entryRepeatsButtonPlus.grid(row=9, column=1)

##
statsRow = 1
statsColumn = 3
##
 
labelTotaltime1 = Label(root, text='Общее время:', font='arial 14 bold')
labelTotaltime1.grid(row=statsRow+1,column=statsColumn, columnspan=2, sticky=E)
labelTotaltime2 = Label(root, text='0.000',font='arial 14 bold')
labelTotaltime2.grid(row=statsRow+1,column=statsColumn+2)

labelRepeats1 = Label(root, text='Повторений:')
labelRepeats1.grid(row=statsRow+2,column=statsColumn, columnspan=2, sticky=E)
labelRepeats2 = Label(root, text='0/'+str(t))
labelRepeats2.grid(row=statsRow+2,column=statsColumn+2)

labelAverage1 = Label(root, text='Среднее время:')
labelAverage1.grid(row=statsRow+3,column=statsColumn, columnspan=2, sticky=E)
labelAverage2 = Label(root, text='0.000')
labelAverage2.grid(row=statsRow+3,column=statsColumn+2)

labelFastest1 = Label(root, text='Минимальное время:', fg='green')
labelFastest1.grid(row=statsRow+4,column=statsColumn, columnspan=2, sticky=E)
labelFastest2 = Label(root, text='0.000', fg='green')
labelFastest2.grid(row=statsRow+4,column=statsColumn+2)

labelSlowest1 = Label(root, text='Максимальное время:', fg='red')
labelSlowest1.grid(row=statsRow+5,column=statsColumn, columnspan=2, sticky=E)
labelSlowest2 = Label(root, text='0.000', fg='red')
labelSlowest2.grid(row=statsRow+5,column=statsColumn+2)

#labelAttempts = Label(root, text="Attempt times:")
#labelAttempts.grid(row=statsRow+2, column=statsColumn-1, sticky=W)


mode=IntVar()
rb = []
rb.append(Radiobutton(root, text='Одиночный', variable=mode, value=1, command=bindOvalClick,indicatoron=0))
rb.append(Radiobutton(root, text='Слyчайно', variable=mode, value=0, command=unBindOvalClick,indicatoron=0))
rb.append(Radiobutton(root, text='Пyть', variable=mode, value=2, command=bindOvalClick,indicatoron=0))
rb[0].grid(row=0, column = 4, sticky=E)
rb[1].grid(row=0, column = 5)
rb[2].grid(row=0, column = 6, sticky=W)

buttonExit = Button(root, text='Выход', command=root.destroy, width= '4')
buttonExit.grid(row=9, column=6)

init()    
root.mainloop()
