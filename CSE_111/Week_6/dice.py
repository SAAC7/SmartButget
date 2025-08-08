import tkinter as tk
from tkinter import Frame,Label,Button
from number_entry import IntEntry
import random

def main():
    root = tk.Tk()
    frm_main = Frame(root)
    root.option_add("Font","Helvetica 16")
    frm_main.master.title("Dice")
    frm_main.pack(padx=3,pady=3,fill=tk.BOTH,expand=1)
    setup_main(frm_main)
    frm_main.mainloop()

def setup_main(frm):
    lbl_sides = Label(frm,text="Enter the number of sides on the dices (2-20)")
    lbl_sides.grid(row=0,column=0)
    ent_sides=IntEntry(frm,width=3,lower_bound=2,upper_bound=20)
    ent_sides.grid(row=0,column=1)
    lbl_dices = Label(frm,text="Enter the number of dices to roll(1-10)")
    lbl_dices.grid(row=1,column=0)
    ent_dices=IntEntry(frm,width=3,lower_bound=1,upper_bound=10)
    ent_dices.grid(row=1,column=1)
    btn_roll=Button(frm,text="Roll IT!!")
    btn_roll.grid(row=2,column=0)
    lbl_roll=Label(frm,text="")
    lbl_roll.grid(row=3,column=0)

    def roll_dice(sides,count):
        sum=0
        roll_text=""
        for roll in range(count):
            die_roll=random.randint(1,sides)
            sum+=die_roll
            roll_text+=f"{die_roll} "
        roll_text += f"Total {sum}"
        return roll_text

    def roll_action():
        try:
            sides = ent_sides.get()
        except:
            lbl_roll.config(text="You must enter a valid number of sides")
            return
        try:
            count = ent_dices.get()
        except:
            lbl_roll.config(text="You must enter a valid number of dices")
            return
        lbl_roll.config(text=roll_dice(sides,count))

    btn_roll.config(command=roll_action)

if __name__ == "__main__":
    main()