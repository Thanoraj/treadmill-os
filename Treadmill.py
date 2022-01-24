from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from time import *
import math
import threading
from tkinter import messagebox

#A function to convert cm, m, in inputs to m
def m_converter(value) :
    u = []
    try :
        u = value.split(' ')
    except :
        return 'Please insert the value with unit'
    unit = u[1]
    value = u[0]
    value = float (value)
    if unit == 'm' :
        value = value
    elif unit == 'cm' :
        value = value / 100
    elif unit == 'in' :
        value = value / 39.37
    else :
        value = 'Wrong input unit'
    return value

#A function to convert kg,lb inputs to kg
def kg_converter(value) :
    try :
        [value,unit] = value.split(' ')
    except :
        return 'Please insert the value with unit'
    value = float (value)
    if unit == 'kg' :
        value = value 
    elif unit == 'lb':
        value = value / 2.205
    else :
        value = 'Wrong input unit'
    return value

def speed(rpm,radius) :
    '''
    A Function to calculate the speed

    Examples:
    >>> speed(1200,'35 cm')
    43.982297150257104
    >>> speed(2500,'0.05 m')
    13.089969389957473
    '''
    #Converting to SI units
    radius = m_converter(radius)

    #Equations to find speed
    angular_velocity = (rpm*2*math.pi)/60
    speed = radius*angular_velocity
    return speed


def distance_walked_or_ran(rpm,radius,duration) :
    '''
    A function to calculate the amount of distance walked or ran

    Examples:
    >>> >>> distance_walked_or_ran(1200,'5 in','600 s')
    9575.593559328809
    >>> distance_walked_or_ran(2000,'4 cm','42 min')
    21111.502632123407
    '''

    #distance traveled in the time different
    distance = speed(rpm,radius)*duration
    return distance

def calories_burnt(rpm,radius,weight,duration) :
    '''
    A function to calculate the burnt calories during the exercise

    Examples :
    >>> calories_burnt(1600,'4.2 cm','52 kg','1.2 h')
    1646.349317093401
    >>> calories_burnt(1600,'4.2 cm','75 lb','45.2 min')
    676.0475639265157
    '''
    #Converting to SI units
    weight = kg_converter(weight)
    
    #the volume of Oxygen needed for walking 1m per min(in ml)
    if speed(rpm,radius) <= 2.2352 :
        v_oxy_exe = 0.1
    else :
        v_oxy_exe = 0.2

    #the volume of Oxygen intaking at rest (in ml)
    v_oxy_rest= 3.5

    #the calories used by 1l of Oxygen (in calories)
    cal_per_1l_of_oxy = 5

    #Equations to calculate calories
    vol_of_oxy_per_kg = v_oxy_exe * (speed(rpm,radius)*60) + v_oxy_rest
    tot_vol_of_oxy = vol_of_oxy_per_kg * weight
    cal_per_min = (tot_vol_of_oxy/1000) * cal_per_1l_of_oxy
    tot_cal = cal_per_min * (duration/60)
    return tot_cal

def steps_counter(rpm,radius,height,duration) :
    #gender wise stride length per inch height
    '''
    A function to calculate the steps walked or ran

    Example :
    >>> steps_counter(1234,'0.045 m','1.21 m','30 min')
    20895.034142273475
    >>> steps_counter(3456,'2 in','123 cm','45 s')
    1624.7030429402012
    ''' 
    #Converting to SI units
    height = m_converter(height)

    #Equations to calculate steps
    stride_len_per_m_in_m = 0.414
    stride_len = stride_len_per_m_in_m*height
    steps_taken = distance_walked_or_ran(rpm,radius,duration) /stride_len
    return steps_taken

#####################################################################################
def keyboard_window(e,ety,window):
    global keyboard_frame
    global num
    num = '0'

    global x
    x += 1
    if x > 1:
        keyboard_frame.grid_forget()

    e_txt = str(ety)
    t_type = e_txt[2:7]


    if t_type == 'label':
        target_lbl.config(text = 'Target\n'+num+' km')

    
    global entry
    entry = ety

    def add(n):
        if t_type == 'frame' :
            global entry
            val = entry.get()
            ind = entry.index(INSERT)
            if n == 'dlt' :
                entry.delete(ind-1)
            
            else:
                if val == '0':
                    if n == '.' :
                        entry.insert(END, n)
                        
                    else :
                        entry.delete(0)
                        entry.insert(ind,str(n))

                else:
                    entry.insert(ind,str(n))

        elif t_type == 'label':
            global num
            n = str(n)
            if n == 'dlt' :
                num = num[0:-1]          
            else:
                if num == '0':
                    if n == '.':
                        num = num+n
                    else :
                        print (n)
                        num = n
                else :
                    num = num + n
                        
            target_lbl.config(text = 'Target\n'+num+' km')

    keyboard_frame = Frame(window, bg = '#000033')
    keyboard_frame.grid(column = 0, row = 0,sticky = S)

    btn7 = Button(keyboard_frame, text = 7, width = 10, height = 2, command = lambda:add(7))
    btn8 = Button(keyboard_frame, text = 8, width = 10, height = 2, command = lambda:add(8))
    btn9 = Button(keyboard_frame, text = 9, width = 10, height = 2, command = lambda:add(9))
    btn4 = Button(keyboard_frame, text = 4, width = 10, height = 2, command = lambda:add(4))
    btn5 = Button(keyboard_frame, text = 5, width = 10, height = 2, command = lambda:add(5))
    btn6 = Button(keyboard_frame, text = 6, width = 10, height = 2, command = lambda:add(6))
    btn1 = Button(keyboard_frame, text = 1, width = 10, height = 2, command = lambda:add(1))
    btn2 = Button(keyboard_frame, text = 2, width = 10, height = 2, command = lambda:add(2))
    btn3 = Button(keyboard_frame, text = 3, width = 10, height = 2, command = lambda:add(3))
    btn_dot = Button(keyboard_frame, text = '.', width = 10, height = 2, command = lambda:add('.'))
    btn0 = Button(keyboard_frame, text = 0, width = 10, height = 2, command = lambda:add(0))
    btn_dlt = Button(keyboard_frame, text = u'\u232B', width = 10, height = 2, command = lambda:add('dlt'))
    btn_ent = Button(keyboard_frame, text = 'Done', width = 10, height = 2, command = keyboard_frame.grid_forget)

    btn7.grid(column = 0, row = 0,padx = (270,10), pady = (10,10))
    btn8.grid(column = 1, row = 0,padx = (0,10), pady = (10,10))
    btn9.grid(column = 2, row = 0,padx = (0,270), pady = (10,10))
    btn4.grid(column = 0, row = 1,padx = (270,10), pady = (0,10))
    btn5.grid(column = 1, row = 1,padx = (0,10), pady = (0,10))
    btn6.grid(column = 2, row = 1,padx = (0,270), pady = (0,10))
    btn1.grid(column = 0, row = 2,padx = (270,10), pady = (0,10))
    btn2.grid(column = 1, row = 2,padx = (0,10), pady = (0,10))
    btn3.grid(column = 2, row = 2,padx = (0,270), pady = (0,10))
    btn_dot.grid(column = 0, row = 3,padx = (270,10), pady = (0,10))
    btn0.grid(column = 1, row = 3,padx = (0,10), pady = (0,10))
    btn_dlt.grid(column = 2, row = 3,padx = (0,270), pady = (0,10))
    btn_ent.grid(column = 1, row = 4)
####################################################################################

def cancel():
    global responce
    responce = messagebox.showwarning('Canceling', 'Do you want to cancel the setup?')
    if responce == 'ok':
        return first.destroy()

def Continue_1():
    Input_file = open('Inputs.txt','w')
    global radius
    radius = float(radius_ety.get())
    grade = float (grade_ety.get())
    if radius > 0 :
        Input_file.write('radius'+':'+str(radius)+selected.get()+' \n'
                     'grade'+':'+str(grade)+'\n')
        Input_file.close()
        
        frame3= Frame(first, bg = '#000033')
        frame3.place(relwidth = 1, relheight = 1)

        text4= 'This device is all set to use'
    
        comp_label = Label(frame3,text=text4,font=font1,bg='#000033',fg='white',bd=0) 
        comp_label.grid(row =0,column=0,pady = (330,280),padx = 190 )

        def Continue():
            first.destroy()
        
        continue_button = Button(frame3,text ='Continue >>',width = 14,command = Continue)
        continue_button.grid(row =1,column=1,sticky=SE)      

    else:
        err_lbl1.config(text='Input correct radius!', bg='#cc0000', fg='white')

def setup():
    frame1.place_forget()
    global frame2
    frame2 = Frame(first,bg = '#000033',width = 800, height = 700)
    frame2.grid(column = 0, row = 0)

    w_n_h_lbl_font = ('Digital-7',25,'bold')

    r_label = Label(frame2,text = 'Radius:',font = w_n_h_lbl_font, width = 15, bg = '#000033', fg = 'white')
    r_label.grid(row = 0, column = 0, pady = (300,10))

    global radius_ety
    radius_ety = Entry(frame2, font = w_n_h_lbl_font, width = 15)
    radius_ety.grid(row = 0, column = 1,sticky = S, pady = 10)
    radius_ety.insert(0, '0')
    radius_ety.bind('<Button-1>', lambda event, entry = radius_ety, window = first : keyboard_window(event, entry,window))

    global selected
    selected = StringVar()
    selected.set(' m')

    r_units = OptionMenu (frame2, selected, ' m' , ' cm', ' in')
    r_units.grid (row = 0, column = 1, sticky = SE, pady = 13)

    global err_lbl1
    err_lbl1 = Label(frame2,text='',bg='#000033',fg='white')
    err_lbl1.grid(row=0,column =2, columnspan = 2, sticky = S, pady = 15, padx = 20)

    grade_label = Label(frame2,text = 'Grade:',font = w_n_h_lbl_font, bg = '#000033', fg = 'white')
    grade_label.grid(row = 1, column = 0, pady = (10,200))

    global grade_ety
    grade_ety = Entry(frame2, font = w_n_h_lbl_font, width = 15)
    grade_ety.grid(row = 1, column = 1,sticky = N, pady = 10)
    grade_ety.insert(0,'0')
    grade_ety.bind('<Button-1>', lambda event, entry = grade_ety, window = first : keyboard_window(event, entry,window))

    continue_button = Button(frame2,text ='Continue >>',width = 12,command = Continue_1)
    continue_button.grid(row = 2, column = 3,columnspan = 2, pady = (59,18), padx =(100,0))

    cancel_button = Button(frame2,text = 'cancel',width = 10,command = cancel)
    cancel_button.grid(row = 2, column = 5, pady = (59,18), padx = (10,30))        

def setup_window():
    global first    
    first = Tk()
    first.geometry('800x700+0+0')
    first.resizable(width = False, height = False)

    global frame1
    frame1 = Frame(first, bg = '#000033')
    frame1.place(relwidth = 1, relheight = 1)

    global font1
    font1 = ('Times new roman',18,'bold')
    text1 = 'This device must be setuped by manufacturer prior to distribute...\n Thus the device will not work properly'

    setupinfo=Label(frame1,text=text1,font=font1,bg='#000033',fg='white',bd=0) 
    setupinfo.grid(column = 0 , row = 0 , columnspan = 2, pady = 300, padx = 60)


    cancel_button = Button(frame1,text ='Cancel',width = 10,command = cancel )
    cancel_button.grid(column = 1,row = 1, padx =10 , pady = (0,20))

    setup_button = Button(frame1,text = 'Start setup',width = 10,command = setup)
    setup_button.grid(row = 1, column = 0,padx = (600,10), pady = (0,20))

    first.mainloop()
#################################################################################

def start_frame():
    #first frame
    global welcome_frame
    welcome_frame = Frame(interface, bg = '#000033')
    welcome_frame.place( relheight = 1 , relwidth = 1 )

    #welcome text label
    welcome_lbl = Label(welcome_frame, text = 'WELCOME',bg = '#000033',
                        fg = 'white', font = ('Digital-7', 50,'bold'))
    welcome_lbl.grid(row = 0, column = 0, pady = (310,220),padx = 300)

    #images for next and back buttons
    global backimage 
    global nextimage
    backimage = PhotoImage(file="sources/back.png")
    nextimage = PhotoImage(file="sources/next.png")

    #button for direct to details frame
    next_button = Button(welcome_frame, image=nextimage, bg = '#000033',bd = 0,
                        activebackground='#000033',height=75,width =75,
                         command = Next)
    next_button.grid(row =1, column = 0, sticky = SE, padx = 35, pady = (0,5))

    
    interface.mainloop()

def Next():
    #details frame
    welcome_frame.place_forget()

    global frame
    frame = Frame(interface,bg = '#000033',width = 800, height = 700)
    frame.grid(column = 0, row = 0)

    w_n_h_lbl_font = ('Digital-7',25,'bold')

    w_lbl = Label(frame,text = 'weight:',font = w_n_h_lbl_font, width = 15, bg = '#000033', fg = 'white')
    w_lbl.grid(row = 0, column = 0, pady = (300,10))

    global w_ety
    w_ety = Entry(frame, font = w_n_h_lbl_font, width = 15)
    w_ety.grid(row = 0, column = 1,sticky = S, pady = 10)
    w_ety.insert(0, '52')
    w_ety.bind('<Button-1>', lambda event, entry = w_ety, window = interface : keyboard_window(event, entry, window)) 

    global w_selected
    w_selected = StringVar()
    w_selected.set(' kg')

    w_units = OptionMenu (frame, w_selected, ' kg' , ' lb')
    w_units.grid (row = 0, column = 1, sticky = SE, pady = 13)

    global err_lbl1
    err_lbl1 = Label(frame,text='',bg='#000033',fg='white')
    err_lbl1.grid(row=0,column =2, columnspan = 2, sticky = S, pady = 15, padx = 20)

    h_lbl = Label(frame,text = 'height:',font = w_n_h_lbl_font, bg = '#000033', fg = 'white')
    h_lbl.grid(row = 1, column = 0, pady = (10,200))

    global h_ety
    h_ety = Entry(frame, font = w_n_h_lbl_font, width = 15)
    h_ety.grid(row = 1, column = 1,sticky = N, pady = 10)
    h_ety.insert(0,'1.78')
    h_ety.bind('<Button-1>', lambda event, entry = h_ety,window = interface : keyboard_window(event, entry, window)) 

    #h_entry.bind('<Button-1>',keyboard_window)
    
    global h_selected
    h_selected = StringVar()
    h_selected.set(' m')

    h_units = OptionMenu (frame, h_selected, ' m' , ' cm' , ' in')
    h_units.grid (row = 1, column = 1, sticky = NE, pady = 13)

    global err_lbl2
    err_lbl2 = Label(frame,text='',bg='#000033',fg='white')
    err_lbl2.grid(row=1,column =2, columnspan = 2, sticky = N, pady = 15, padx = 20)


    b_btn = Button (frame, image = backimage, height = 75, width = 75, bd = 0, bg = '#000033', activebackground = '#000033', command = start_frame)
    b_btn.grid(row = 2, column = 3,columnspan = 2, pady = (7,18), padx =(100,0))

    n_btn = Button (frame, image = nextimage, height = 75, width = 75, bd = 0, bg = '#000033', activebackground = '#000033', command = Continue)
    n_btn.grid(row = 2, column = 5, pady = (7,18), padx = 21)

def Continue():
    #checking for validity and converting them to float
    global weight
    weight = w_ety.get()+w_selected.get()
    weight_f = float(w_ety.get())

    global height
    height = h_ety.get()+h_selected.get()
    height_f = float(h_ety.get())

    if weight_f <=0 and height_f <= 0 :
        err_lbl1.config(text='Input correct weight!',bg='#cc0000',fg='white')
        err_lbl2.config(text='Input correct height!',bg='#cc0000', fg='white')
            
    elif weight_f <= 0 and height_f > 0 :
        err_lbl1.config(text='Input correct weight!', bg='#cc0000', fg='white')
        err_lbl2.config(text = '', bg = '#000033')

    elif height_f <= 0 and weight_f > 0 :
        err_lbl2.config(text='Input correct height!',bg='#cc0000',fg='white')
        err_lbl1.config( text = '', bg = '#000033')

    #check all values and redirect to output frame
    else :
        def increase():
            global rpm
            rpm += 50
            canvas.itemconfigure(rpm_output_lbl,text = str(rpm))
            
            global speed1
            speed1 = speed(rpm,radius)
            speed_lbl.config(text = 'SPEED\n'+str('%.2f'%speed1)+' m/s')

            #changing the button states
            dec_button.config(state = ACTIVE)
            pause_btn.config(state = ACTIVE)

            #start the calculation of distance, calories and steps in background
            threading.Thread(target = update).start()
            
        def decrease():
            global rpm
            rpm -= 50
            canvas.itemconfigure(rpm_output_lbl, text = str(rpm))

            global speed1
            speed1 = speed(rpm,radius)
            speed_lbl.config(text = 'SPEED\n'+str('%.2f'%speed1)+' m/s')

            #changing the button states
            dec_button.config(state = ACTIVE)
            pause_btn.config(state = ACTIVE)

            #start the calculation of distance, calories and steps in background
            threading.Thread(target = update).start()

            if rpm == 0:
                dec_button.config(state = DISABLED)
                pause_btn.config(state = DISABLED)

        def pause():
            #set the rpm to 0 when pause button is clicked and update it label
            global rpm
            rpm = 0
            canvas.itemconfigure(rpm_output_lbl,text = str(rpm))

            #calculate the speed for new rpm and update it to label
            global speed1
            speed1 = speed(rpm,radius)
            speed_lbl.config(text = 'SPEED\n'+str(speed1)+' m/s' )

            #start the calculation of distance, calories and steps in background
            threading.Thread(target = update).start()
            
            #set the decrease button state to disabled
            dec_button.config(state = DISABLED)
            start_btn.config(state = ACTIVE)
            pause_btn.config(state = DISABLED)
            inc_button.config(state = DISABLED)
            dec_button.config(state = DISABLED)

            global num
            if remaining == None:
                num = 0

            elif remaining > 0:
                num = remaining

            elif remaining == 0:
                num = remaining - 1

            else :
                num = remaining   

        def stop():
            #set the rpm to 0 when the stop button is clicked
            global rpm
            rpm = 0
            canvas.itemconfigure(rpm_output_lbl,text = str(rpm))

            #calculate the new speed for new rpm
            global speed1
            speed1 = speed(rpm,radius)
            speed_lbl.config(text = 'SPEED\n'+str(speed1)+' m/s' )

            #resetting all
            global d_tot, c_tot, s_tot, t_tot, num
            d_tot = 0
            c_tot = 0
            s_tot = 0
            t_tot = 0

            canvas.itemconfigure(dis_output_lbl,text = str(int(d_tot))+' m')            
            canvas.itemconfigure(cal_output_lbl,text = str(int(c_tot))+' cal')
            canvas.itemconfigure(steps_output_lbl,text = str(int(s_tot)))
            canvas.itemconfigure(time_lbl,text = str(int(t_tot))+' s')

            start_btn.config(state = ACTIVE)
            stop_btn.config(state = DISABLED)
            pause_btn.config(state = DISABLED)
            inc_button.config(state = DISABLED)
            dec_button.config(state = DISABLED)
            back_btn.config(state = ACTIVE)

            global num
            num = None
            target_lbl.config(text = u'\u26F3'+'\n'+'Set your target' )
            target_lbl.bind('<Button-1>', lambda event, entry = target_lbl, window = interface : keyboard_window(event, entry, window)) 

        #A function to calculate distance, calories and steps in background
        def update():
            #start a timer first loop
            s_time = time()
            #creating a condition for run the loop
            if speed1 > 0 :
                speed2 = speed1
            #creating a condition to stop the loop when rpm is changed
            else :
                speed2 = -1

            t_dif2 = 0
            while speed2 == speed1 :
                #end the timer calculating the total time and update it to label
                e_time = time()
                t_dif = e_time - s_time + t_dif2
                global t_tot
                t_tot += t_dif
                canvas.itemconfigure(time_lbl,text = str(int(t_tot))+' s')

                #calculating the distance and update it to label
                dis = distance_walked_or_ran(rpm,radius,t_dif)
                global d_tot
                d_tot += dis
                canvas.itemconfigure(dis_output_lbl,text = str(int(d_tot))+' m')

                if num == None :
                    target_lbl.config(text = 'You are doing well\n'+'Keep Running',font = ('Times new roman',30,'bold'), width = 14, height = 4 )
                    
                elif d_tot/1000 <= float(num) :
                    global remaining
                    remaining = float(num) - d_tot/1000
                    target_lbl.config(text = str('%.3f'%remaining)+'\n'+'km remaining' )

                else :
                    if num == 0:
                        target_lbl.config(text = 'You are doing well\n'+'Keep Running',font = ('Times new roman',30,'bold'), width = 14, height = 4 )

                    else:
                        target_lbl.config(text = 'Congratulations'+'\n'+'Goal reached',font = ('Times new roman',31,'bold'), width = 13 )
                
                #calculating the calories and update to label
                cal = calories_burnt(rpm,radius,weight,t_dif)
                global c_tot
                c_tot += cal
                canvas.itemconfigure(cal_output_lbl,text = str(int(c_tot))+' cal')

                #calculating the steps and update it to label
                steps = steps_counter(rpm,radius,height,t_dif)
                global s_tot
                s_tot += steps
                canvas.itemconfigure(steps_output_lbl,text = str(int(s_tot)))

                #start the timer next loop
                s_time = time()
                t_dif2 = s_time - e_time

                sleep(0.02)

        #function for clock
        def clock() :
            w_d = strftime('%A')
            dt = strftime('%d')
            mnt = strftime('%b')
            yr = strftime('%Y')
            hr = strftime('%I')
            mn = strftime('%M')
            sec = strftime('%S')
            am_pm = strftime('%p')
            status_lbl.config(text =w_d+'   '+dt+'th of '+mnt+' '+yr+'     '+hr+':'+mn+':'+sec+' '+am_pm)
            status_lbl.after(1000,clock)

        #Animating function for background image
        def animate(counter):
            canvas.itemconfig(image, image = sequence[counter])
            if speed1 == 0:
                interface.after(5, lambda: animate((counter) % len(sequence)))

            else :
                interface.after(int(100/speed1), lambda: animate((counter+1) % len(sequence)))

        #configure button for running
        def start():
            start_btn.config(state = DISABLED)
            back_btn.config(state = DISABLED)
            inc_button.config(state = ACTIVE)
            stop_btn.config(state = ACTIVE)
            target_lbl.unbind('<Button-1>')
            
            if num == None :
                target_lbl.config(text = u'\u26F3'+'\n'+'Set your target' )
                target_lbl.bind('<Button-1>', lambda event, entry = target_lbl,window = interface : keyboard_window(event, entry, window)) 
            else:
                Num = float(num)   
                if Num == 0:
                    target_lbl.config(text = 'You are doing well\n'+'Keep Running',font = ('Times new roman',30,'bold'), width = 14, height = 4 )

                elif Num > 0:
                    target_lbl.config(text = str('%.3f'%Num)+'\n'+'km remaining' )

                else :
                    target_lbl.config(text = 'Congratulations'+'\n'+'Goal reached' )

            if rpm == 0 :
                dec_button.config(state = DISABLED)
                pause_btn.config(state = DISABLED)
            else :
                dec_button.config(state = ACTIVE)
                pause_btn.config(state = ACTIVE)
            
        #fonts for label and outputs
        out_frame_font = ('Digital-7',50,'bold')
        out_label_font = ('Digital-7',30,'bold')

        def output():
            global canvas
            canvas = Canvas(interface, width = 800, height = 700, highlightthickness = 0)
            canvas.place(relheight = 1, relwidth = 1 )

            global sequence
            sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(r'sources/running8.gif'))]

            global image
            image = canvas.create_image(0,0,image=sequence[1],anchor = NW)
            animate(1)

            #a label to show running time
            global time_lbl
            time_lbl = canvas.create_text(100,50,anchor = NW,text = str(int(t_tot))+' s',fill = 'white', font = out_frame_font )

            #label to show the current RPM
            global rpm_output_lbl
            rpm_l = canvas.create_text(50,150,text='RPM',fill= 'white',anchor = NW, font = out_label_font)
            rpm_output_lbl = canvas.create_text(50,250,anchor = NW, text=str(rpm),fill = 'white', font = out_frame_font)

            #label to show the current speed            
            global speed_lbl
            speed_lbl = Label(interface, text='SPEED\n'+'0 m/s',width = 10, height = 3, relief = 'groove', bd = 5,
                              font = out_frame_font, fg = 'white', bg = '#000033')
            speed_lbl_window = canvas.create_window(230,300, anchor = NW, window = speed_lbl)

            global target_lbl
            target_lbl = Label(interface, text=u'\u26F3'+'\n'+'Set your target',width = 11, height = 3, relief = 'groove', bd = 5,
                              font = ('Times new roman',37,'bold'), fg = 'white', bg = '#000033')
            target_lbl_window = canvas.create_window(230, 50, anchor = NW, window = target_lbl)
            target_lbl.bind('<Button-1>', lambda event, entry = target_lbl,window = interface : keyboard_window(event, entry, window)) 

            #images for increase and decrease button
            global inc_image
            inc_image = PhotoImage(file="sources/increase.png")
            global dec_image
            dec_image = PhotoImage(file="sources/decrease.png")

            #button for increase RPM
            global inc_button
            inc_button = Button(interface, image=inc_image, bg = '#333654',bd = 0, activebackground = '#333654', height=30,
                                width = 30, state = DISABLED, command = increase)
            inc_button_window = canvas.create_window(180, 253, anchor = NW, window = inc_button )

            #button for decrease RPM
            global dec_button
            dec_button = Button(interface, image=dec_image, bg = '#333654',bd = 0, activebackground = '#333654', height=30,
                                width =30,state = DISABLED,command = decrease)
            dec_button_window = canvas.create_window(180, 287, anchor = NW, window = dec_button )


            # labels for show the distance
            global dis_output_lbl
            dis_l = canvas.create_text(50,400,anchor = NW, text ='DISTANCE',font = out_label_font,fill = 'white')
            dis_output_lbl = canvas.create_text(50,500,anchor = NW, text='0 m',fill = 'white',font = out_frame_font)

            #labels for show calories
            global cal_output_lbl
            cal_l = canvas.create_text(600,150,anchor = NW,text ='CALORIES',font = out_label_font,fill = 'white')
            cal_output_lbl = canvas.create_text(600,250,anchor = NW, text='0 cal',fill = 'white',font = out_frame_font)
                                   
            #labels for show steps
            global steps_output_lbl
            steps_l = canvas.create_text(600,400,anchor = NW,text ='STEPS',font = out_label_font,fill = 'white')
            steps_output_lbl = canvas.create_text(600,500,anchor = NW,text='0',fill = 'white',font = out_frame_font)
                                     
            global stop_img, play_img, pause_img
            stop_img = PhotoImage(file="sources/stop.png")
            play_img = PhotoImage(file="sources/play.png")
            pause_img = PhotoImage(file="sources/pause.png")

            #button for start running
            global start_btn
            start_btn = Button(interface,image = play_img, bg = '#333654',activebackground = '#333654', bd = 0,command = start)
            start_button_window = canvas.create_window(250, 600, anchor = NW, window = start_btn )

            #button for pause running
            global pause_btn
            pause_btn = Button(interface,image =  pause_img, bg = '#333654', bd = 0,
                               activebackground = '#333654', state = DISABLED, command = pause)
            pause_button_window = canvas.create_window(350, 600, anchor = NW, window = pause_btn )

            #button for stop running and reset data
            global stop_btn
            stop_btn = Button(interface,image = stop_img,bg = '#333654', activebackground = '#333654', bd = 0,
                              width = 50, height = 50, state = DISABLED, command = stop)
            stop_button_window = canvas.create_window(450, 600, anchor = NW, window = stop_btn )

            global back_btn
            back_btn = Button (interface, image = backimage, height = 75, width = 75, bd = 0, bg = '#333654', activebackground = '#333654', command = Next)
            back_btn_window = canvas.create_window(600, 590, anchor = NW, window = back_btn)
            
            global status_lbl
            status_lbl = Label(interface, text = '', font = ('Digital-7', 15,'bold'),anchor = W, bg = '#000033', fg = '#009900', width = 89)
            status_lbl_window = canvas.create_window(0,673,anchor = NW, window = status_lbl)

        #redirecting to output frame        
        output()
        clock()

#assigning start values
x = 0
speed1 = 0
rpm = 0
d_tot = 0
c_tot = 0
s_tot = 0
t_tot = 0
num = None

#open and read the inputs file
para_file = open('Inputs.txt','r')
line=[]
line = para_file.readlines()

#checking that the device is setupped or not 
if len(line) == 0:
    para_file.close()
    #direct to setup window for setting up the device
    setup_window()
    x = 0
    para_file = open('Inputs.txt','r')
    line = []
    line = para_file.readlines()

rad = [0]
#read the inputs file and assign names for the values 
for i in range (len(line)):
    parameters = line[i].split(':')

    if parameters[0] == 'radius':
        rad = parameters[1].split(' ')
        radius = parameters[1]

    elif parameters[0] == 'grade':
        grade = float(parameters[1])

if float(rad[0]) > 0:
    #starting the program and setting up window
    interface = Tk()
    interface.title('3T Treadmill')
    interface.geometry('800x700+0+0')
    interface.resizable(width = False, height = False)
    start_frame()
          
#close the input file
para_file.close()
