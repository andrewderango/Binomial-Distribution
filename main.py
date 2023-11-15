from tkinter import *
import math
import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline

root = Tk()
root.resizable(False, False)
root.geometry("675x500")
root.title('Binomial Distribution Calculator')
root.configure(background="#151326")

def getProbability():
    global lower
    global upper
    global cumulativeProbability
    global finalResultLabelsActive
    #global finalProbabilityLabel
    global inverseProbabilityLabel
    global entry1_error
    global entry2_error
    global entry3_error
    global entry4_error
    global percentage_circle
    global circle_image_subsample
    global attempts
    global probability
    inputEntryValid = 1

    try:
        #finalProbabilityLabel.place_forget()
        inverseProbabilityLabel.place_forget()
    except NameError:
        pass

    try:
        entry1_error.place_forget()
    except NameError:
        pass
    try:
        probability = float(entry1.get())
        entry1.configure(bg="white")
        if probability >= 1 or probability <= 0:
            probability = int('str')
    except ValueError:
        entry1.configure(bg="red")
        entry1_error = Label(font=("TkDefaultFont", 9), text="Must be between 0-1", fg="red", bg="#151326")
        entry1_error.place(x=131.25, y=155, anchor=CENTER)
        finalProbabilityBigNum.configure(text="-- %")
        finalProbabilityPrecise.configure(text="--")
        inputEntryValid = 0

    try:
        entry2_error.place_forget()
    except NameError:
        pass
    try:
        attempts = int(entry2.get())
        entry2.configure(bg="white")
        if attempts < 1:
            attempts = int('str')
    except ValueError:
        entry2.configure(bg="red")
        entry2_error = Label(font=("TkDefaultFont", 9), text="Must be a positive integer", fg="red", bg="#151326")
        entry2_error.place(x=268.75, y=155, anchor=CENTER)
        finalProbabilityBigNum.configure(text="-- %")
        finalProbabilityPrecise.configure(text="--")
        inputEntryValid = 0

    try:
        entry3_error.place_forget()
    except NameError:
        pass
    try:
        lower = int(entry3.get())
        entry3.configure(bg="white")
        if lower < 0:
            lower = int('str')
        if lower > attempts:
            entry3.configure(bg="red")
            entry3_error = Label(font=("TkDefaultFont", 9), text="Can not be greater than 'attempts'", fg="red", bg="#151326")
            entry3_error.place(x=406.25, y=155, anchor=CENTER)
            finalProbabilityBigNum.configure(text="-- %")
            finalProbabilityPrecise.configure(text="--")
            inputEntryValid = 0
    except ValueError:
        entry3.configure(bg="red")
        entry3_error = Label(font=("TkDefaultFont", 9), text="Must be a positive integer", fg="red", bg="#151326")
        entry3_error.place(x=406.25, y=155, anchor=CENTER)
        finalProbabilityBigNum.configure(text="-- %")
        finalProbabilityPrecise.configure(text="--")
        inputEntryValid = 0

    try:
        entry4_error.place_forget()
    except NameError:
        pass
    try:
        upper = int(entry4.get())
        entry4.configure(bg="white")
        if upper < 0:
            upper = int('str')
        if upper > attempts:
            entry4.configure(bg="red")
            entry4_error = Label(font=("TkDefaultFont", 9), text="Can not be greater than 'attempts'", fg="red", bg="#151326")
            entry4_error.place(x=543.75, y=155, anchor=CENTER)
            finalProbabilityBigNum.configure(text="-- %")
            finalProbabilityPrecise.configure(text="--")
            inputEntryValid = 0
        if upper < lower:
            entry4.configure(bg="red")
            entry4_error = Label(font=("TkDefaultFont", 9), text="Can not be less than 'lower bound'", fg="red", bg="#151326")
            entry4_error.place(x=543.75, y=155, anchor=CENTER)
            finalProbabilityBigNum.configure(text="-- %")
            finalProbabilityPrecise.configure(text="--")
            inputEntryValid = 0       
    except ValueError:
        entry4.configure(bg="red")
        entry4_error = Label(font=("TkDefaultFont", 9), text="Must be a positive integer", fg="red", bg="#151326")
        entry4_error.place(x=543.75, y=155, anchor=CENTER)
        finalProbabilityBigNum.configure(text="-- %")
        finalProbabilityPrecise.configure(text="--")
        inputEntryValid = 0

    if inputEntryValid == 0:
        percentage_circle.place_forget()
        circle_image = PhotoImage(file=os.path.join(current_directory, "Images/Percentage Images/0%.png"))
        circle_image_subsample = circle_image.subsample(7)
        percentage_circle = Label(root, image=circle_image_subsample, bg="#151326")
        percentage_circle.pack()
        percentage_circle.place(x=337.5, y=340, anchor=CENTER)
        finalProbabilityBigNum.tkraise()
        finalProbabilityPrecise.tkraise()
        circle_probability_title.tkraise()
        return None

    cumulativeProbability = 0
    for possibleSuccesses in range(upper+1-lower):
        currentSuccess = possibleSuccesses + lower
        singularProbability = (math.factorial(attempts)/(math.factorial(currentSuccess) * math.factorial(attempts-currentSuccess))) * probability**currentSuccess * (1-probability)**(attempts-currentSuccess)
        #slowPrint(str(currentSuccess) + ': ' + str(round(singularProbability*100,2)) + '%\n')
        cumulativeProbability += singularProbability

    #finalProbabilityLabel = Label(text='The probability of getting between ' + str(lower) + ' and ' + str(upper) + ' successes is ' + str(round(cumulativeProbability*100,4)) + '%',fg="#00A5EC",bg="#151326")
    #finalProbabilityLabel.place(x=337.5,y=400,anchor=CENTER)
    if 1/cumulativeProbability < 10:
        inverseProbabilityLabel = Label(text='This is equivalent to 1 in ' + str(round(1/cumulativeProbability,1)),fg="#00A5EC",bg="#151326")
    else:
        inverseProbabilityLabel = Label(text='This is equivalent to 1 in ' + str(int(1/cumulativeProbability)),fg="#00A5EC",bg="#151326")
    inverseProbabilityLabel.place(x=337.5,y=450,anchor=CENTER)

    percentage_circle.place_forget()

    percentages = [0,0.5,2,5,10,15,20,23,25,27,30,35,40,45,48,50,52,55,60,65,70,73,75,77,80,85,90,95,98,99.5,100]
    perc_prob_differences = []
    for percentageIndex in range(len(percentages)):
        perc_prob_differences.append(abs(cumulativeProbability*100 - percentages[percentageIndex]))

    circle_image = PhotoImage(file=os.path.join(current_directory, "Images/Percentage Images/" + str(percentages[perc_prob_differences.index(min(perc_prob_differences))]) + "%.png"))
    circle_image_subsample = circle_image.subsample(7)
    percentage_circle = Label(root, image=circle_image_subsample, bg="#151326")
    percentage_circle.pack()
    percentage_circle.place(x=337.5, y=340, anchor=CENTER)

    finalProbabilityBigNum.configure(text=str(round(cumulativeProbability*100,1)) + "%")
    finalProbabilityPrecise.configure(text=str(round(cumulativeProbability*100,5)) + "%")

    finalProbabilityBigNum.tkraise()
    finalProbabilityPrecise.tkraise()
    circle_probability_title.tkraise()

    hist_button = Button(fg="#151326",highlightbackground="white",text="Show PDF",width=15,height=2,font=("TkDefaultFont", 11),command=show_hist)
    hist_button.place(x=550,y=315,anchor=CENTER)

    cdf_button = Button(fg="#151326",highlightbackground="white",text="Show CDF",width=15,height=2,font=("TkDefaultFont", 11),command=show_cdf)
    cdf_button.place(x=550,y=365,anchor=CENTER)

def show_cdf():
    global attempts
    global probability
    global lower
    global upper

    plt.style.use('ggplot')

    hist_x = []
    hist_y = []
    hist_c = []

    for attempts_ticker in range(attempts + 1):
        hist_x.append(attempts_ticker)

    for cumulative_probability_ticker in range(attempts + 1):
        try:
            hist_y.append((math.factorial(attempts)/(math.factorial(cumulative_probability_ticker) * math.factorial(attempts - (cumulative_probability_ticker)))) * probability**(cumulative_probability_ticker) * (1-probability)**(attempts - (cumulative_probability_ticker)) + hist_y[cumulative_probability_ticker - 1])
        except IndexError:
            hist_y.append((math.factorial(attempts)/(math.factorial(cumulative_probability_ticker) * math.factorial(attempts - (cumulative_probability_ticker)))) * probability**(cumulative_probability_ticker) * (1-probability)**(attempts - (cumulative_probability_ticker)))

    for below_lower in range(lower):
        hist_c.append("navy")
    for between_bounds in range(upper - lower + 1):
        hist_c.append("red")
    for above_upper in range(attempts - upper):
        hist_c.append("navy")

    X_Y_Spline = make_interp_spline(hist_x, hist_y)
    X_ = np.linspace(min(hist_x), max(hist_x), 500)
    Y_ = X_Y_Spline(X_)

    plt.plot(X_, Y_, color="Black")
    plt.fill_between(X_, Y_, color='Blue', alpha=0.25)
    #plt.bar(hist_x, hist_y, color=hist_c, alpha=0.25)
    plt.title('Cumulative Probability Distribution')
    plt.xlabel('Success Quantity')
    plt.ylabel('Cumulative Frequency')
    plt.tight_layout()
    plt.show()

def show_hist():
    global attempts
    global probability
    global lower
    global upper

    plt.style.use('ggplot')

    hist_x = []
    hist_y = []
    hist_c = []

    for attempts_ticker in range(attempts + 1):
        hist_x.append(attempts_ticker)

    for singular_probability_ticker in range(attempts + 1):
        hist_y.append((math.factorial(attempts)/(math.factorial(singular_probability_ticker) * math.factorial(attempts - (singular_probability_ticker)))) * probability**(singular_probability_ticker) * (1-probability)**(attempts - (singular_probability_ticker)))

    for below_lower in range(lower):
        hist_c.append("navy")
    for between_bounds in range(upper - lower + 1):
        hist_c.append("red")
    for above_upper in range(attempts - upper):
        hist_c.append("navy")

    X_Y_Spline = make_interp_spline(hist_x, hist_y)
    X_ = np.linspace(min(hist_x), max(hist_x), 500)
    Y_ = X_Y_Spline(X_)

    plt.plot(X_, Y_, color="Black")
    # plt.fill_between(X_, Y_,
    #                 where=(lower > X_),
    #                 interpolate=True, color='Red', alpha=0.25)
    # plt.fill_between(X_, Y_,
    #                 where=(upper < X_),
    #                 interpolate=True, color='Red', alpha=0.25)
    plt.bar(hist_x, hist_y, color=hist_c, alpha=0.25)
    plt.title('Probability Distribution')
    plt.xlabel('Success Quantity')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def main():
    current_directory = os.path.dirname(__file__)
    
    probLabel = Label(font=("TkDefaultFont", 9),text='Success probability',fg="#00A5EC",bg="#151326")
    probLabel.place(x=131.25,y=105,anchor=CENTER)
    
    entry1 = Entry(root, borderwidth=3, justify=CENTER, relief=SUNKEN, width=7)
    entry1.place(x=131.25,y=130,anchor=CENTER)
    
    attemptsLabel = Label(font=("TkDefaultFont", 9),text='Attempts',fg="#00A5EC",bg="#151326")
    attemptsLabel.place(x=268.75,y=105,anchor=CENTER)
    
    entry2 = Entry(root, borderwidth=3, justify=CENTER, relief=SUNKEN, width=7)
    entry2.place(x=268.75,y=130,anchor=CENTER)
    
    lowerLabel = Label(font=("TkDefaultFont", 9),text='Lower bound',fg="#00A5EC",bg="#151326")
    lowerLabel.place(x=406.25,y=105,anchor=CENTER)
    
    entry3 = Entry(root, borderwidth=3, justify=CENTER, relief=SUNKEN, width=7)
    entry3.place(x=406.25,y=130,anchor=CENTER)
    
    upperLabel = Label(font=("TkDefaultFont", 9),text='Upper bound',fg="#00A5EC",bg="#151326")
    upperLabel.place(x=543.75,y=105,anchor=CENTER)
    
    entry4 = Entry(root, borderwidth=3, justify=CENTER, relief=SUNKEN, width=7)
    entry4.place(x=543.75,y=130,anchor=CENTER)
    
    circle_image = PhotoImage(file=os.path.join(current_directory, "Images/Percentage Images/0%.png"))
    circle_image_subsample = circle_image.subsample(7)
    percentage_circle = Label(root, image=circle_image_subsample, bg="#151326")
    percentage_circle.pack()
    percentage_circle.place(x=337.5, y=340, anchor=CENTER)
    
    circle_probability_title = Label(text="PROBABILITY", font=("TkDefaultFont", 14), fg="#555555", bg="#151326")
    circle_probability_title.place(x=337.5, y=365, anchor=CENTER)
    
    finalProbabilityBigNum = Label(text="-- %", font=("TkDefaultFont", 33, "bold"), fg="#00A5EC", bg="#151326")
    finalProbabilityBigNum.place(x=337.5, y=330, anchor=CENTER)
    
    finalProbabilityPrecise = Label(text="--", font=("TkDefaultFont", 9), fg="#383838", bg="#151326")
    finalProbabilityPrecise.place(x=337.5, y=400, anchor=CENTER)
    
    title = Label(font=("TkDefaultFont", 30, "bold"),text='Binomial Distribution Calculator',background="#151326",foreground="#00A5EC")
    title.place(x=337.5,y=50,anchor=CENTER)
    
    calc_probability_button = PhotoImage(file=os.path.join(current_directory, "Images/calculate_probability.png"))
    calc_button_subsample = calc_probability_button.subsample(1)
    probability_button = Button(root, image=calc_button_subsample, highlightbackground="#151326", padx = 0, pady = 0, command=getProbability)
    probability_button.place(x=337.5, y=205, anchor=CENTER)
    
    #calc_button = Button(fg="#151326",highlightbackground="white",text="Calculate Probability",width=20,height=3,font=("TkDefaultFont", 13, "bold"),command=getProbability)
    #calc_button.place(x=337.5,y=210,anchor=CENTER)
    
    root.mainloop()

if __name__ == '__main__:
    main()
