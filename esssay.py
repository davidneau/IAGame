from tkinter import *
windowItem1 = Tk()
windowItem1.title("Item1")
WaitState = IntVar()
def submit():
      WaitState.set(1)
      print("submitted")
button = Button(windowItem1, text="Submit", command=submit)
button.grid(column=0, row=1)

print("waiting...")
button.wait_variable(WaitState)
print("done waiting.")
windowItem1.mainloop()
