# Author: Shubham Waghe
# Roll No: 13MF3IM17
# Description: WSD-II Assignment-1
import numpy as np
import matplotlib.pyplot as plt
from random import gauss
import Tkinter as tk
import math

# Given data
READINGS_EACH_DAY = 400
desired_limit = 0.05
p = 0.2
RANGE_VALUE = 3
PLOT_RANGE = 2*p
#Stopping criteria
NO_OF_DAYS = 100

GLOBAL_OBSERVATIONS = []

# Function to calculate sigma
def get_sigma(p):
    sigma = math.sqrt( (p*(1-p)/READINGS_EACH_DAY ))
    return sigma

def get_number_of_days(p):
    n = get_n(p)
    return roundup(n)/READINGS_EACH_DAY

def roundup(x):
    return int(math.ceil(x / READINGS_EACH_DAY*1.0)) * READINGS_EACH_DAY

def get_l(p):
    l = p*desired_limit
    return l

def get_n(p):
    l = get_l(p)
    n = (3.84*p*(1-p))/(l**2)
    return n

def get_accuracy(p, n):
    x = (3.84*p*(1-p))/(n)
    return math.sqrt(x)

days_plotted = 0
plotting_done = False

#Final plot
plt.title("P - Chart :: Shubham Waghe")
plt.xlabel("Mean (p)")
plt.ylabel("Days")

while days_plotted <= NO_OF_DAYS:

    sigma, num_days = get_sigma(p), get_number_of_days(p)
    print "***********************************************************************"
    print "p = ",p, " n = ", get_n(p), " sigma = ", sigma, " Number of days: ", num_days

    # directly taking x<bar> mu and variance/n
    random_numbers = []
    for i in xrange(num_days):
        observations = [gauss(0.2, 0.02) for i in range(NO_OF_DAYS)]
        random_numbers.append(np.mean(observations))
        
    # print random_numbers

    N = len(GLOBAL_OBSERVATIONS)
    t_observations = N + len(random_numbers)
    axes = plt.axis([0, t_observations + 1, 0, PLOT_RANGE])

    ucl, lcl = p + RANGE_VALUE*sigma, p - RANGE_VALUE*sigma
    print "UCL: ", ucl, " LCL: ", lcl
    print "***********************************************************************"

    m_line = plt.axhline(y = p, color='b', linestyle = None)
    ucl_line = plt.axhline(y = ucl, color='r', linestyle = '--')
    lcl_line = plt.axhline(y = lcl, color='r', linestyle = '--')

    offset_length = days_plotted
    for i in range(len(random_numbers)):
        c_pt = plt.scatter(offset_length+i+1, random_numbers[i])
        GLOBAL_OBSERVATIONS.append(random_numbers[i])
        days_plotted += 1
        if random_numbers[i] > ucl or random_numbers[i] < lcl:
            plt.pause(0.05)
            print
            print "###################################################"
            print "Obeservation - Out of Control: ", random_numbers[i]
            print "###################################################"
            p = np.mean(GLOBAL_OBSERVATIONS)
            break
        if days_plotted == NO_OF_DAYS:
            plotting_done = True
            break
        plt.pause(0.05)

    if plotting_done: break
    else:
        axes = plt.axis([0, t_observations + 1, 0, PLOT_RANGE])
        m_line.remove()
        ucl_line.remove()
        lcl_line.remove()
        print

root = tk.Tk()
root.geometry("300x200+100+100")
root.title("Final Results")

revised_p = np.mean(GLOBAL_OBSERVATIONS)
accuracy = get_accuracy(revised_p, get_n(revised_p))
p_accuracy = "{:.2f}".format(accuracy*100)

heading_label = tk.Label(root, text="Results", height=2, width=100, font=("Helvetica", 14)).pack()
p_label = tk.Label(root, text="Revised p : {:.6f}".format(revised_p), height=0, width=100).pack()
accuracy_label = tk.Label(root, text="Accuracy : {0}".format(p_accuracy + " %"), height=0, width=100).pack()

b = tk.Button(root, text="Close", command=exit).pack(padx = 10, pady = 20)
root.mainloop()
while True:
    plt.pause(0.05)