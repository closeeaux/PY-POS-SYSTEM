import os
import sys
import subprocess
import time
import webbrowser
import __main__ as main
from tkinter import END, Button, Tk, TkVersion
import tkinter
import numpy as np
from colorama import Fore
from colorama import Style


try:
    MyProducts = np.load('my_file.npy',allow_pickle='TRUE').item()

except FileNotFoundError:
    MyProducts={}
    np.save('my_file.npy', MyProducts)

np.save('my_file.npy', MyProducts)

fullPrice = 0
productList = []

def create_price_list_html(product_dict, fullPrice):
    # Define the HTML template for the price list
    html_template = """
        <html>
        <head>
        </head>
        <body>
        
        <h2>Price List</h2>
        
        <table style="font-family: arial, sans-serif; border-collapse: collapse; width: 100%;">
            <tr style="background-color: #dddddd;">
                <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Product</th>
                <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Price</th>
            </tr>
            {rows}
        </table>
            Full Price: {fullPrice:.2f} €
        </body>
        </html>
        """

    # Create the rows for the HTML table
    rows = ""
    for product, amount in product_dict.items():
        price = round(float(MyProducts[product]) * amount, 2)
        rows += f"<tr><td>{product} x {amount}</td><td>{price:.2f} €</td></tr>"

    # Replace the placeholder in the HTML template with the rows and fullPrice
    html = html_template.format(rows=rows, fullPrice=fullPrice)

    # Save the HTML to a file
    with open("price_list.html", "w") as f:
        f.write(html)

    # Open the HTML file in the default web browser
    webbrowser.open("price_list.html")

def finish():   
        global fullPrice
        global productList
        if not productList:
            print(f" {Fore.RED}You need to enter at least one product{Style.RESET_ALL}")
        else:
            warenkorb = {}
            for i in productList:

                if i in warenkorb:
                    warenkorb[i] += 1
                else:
                    warenkorb[i] = 1
                
                listbox.delete(0, END)  # clear listbox   
            create_price_list_html(warenkorb, fullPrice)            
            productList = []
            fullPrice = 0.0     
def Create():
    def on_submit():
        price = (entry2.get())
        name = (entry1.get())
        window.destroy()
        try:
            global MyProducts
            os.system('cls')
            MyProducts[name] = float(price)
            np.save('my_file.npy', MyProducts)
        except KeyError:
            print(f" {Fore.RED} This Product maybe allready exist{Style.RESET_ALL}")
        except ValueError:
            print(f" {Fore.RED} The Price/Name has a false format{Style.RESET_ALL}")

    window = tk.Tk()
    window.title("Value Entry")
    window.geometry("230x100")
    window.eval('tk::PlaceWindow . center')
    entry1 = tk.Entry(window)
    entry1.grid(row=0, column=1)

    tk.Label(window, text="Name").grid(row=0, column=0)
    tk.Label(window, text="Price").grid(row=1, column=0)
    entry2 = tk.Entry(window)
    entry2.grid(row=1, column=1)

    submit_button = tk.Button(window, text="Bestätigen", command=on_submit)
    submit_button.grid(row=2, column=0, columnspan=2)

def ProductEnter(Productenter, Amount):  
        global fullPrice 
        global productList
        try:
            global fullPrice
            global MyProducts
            if Productenter in MyProducts:
                Amount = 1
                if Amount != "":
                    fullPrice += float(MyProducts[Productenter]) * float(Amount)
                    for i in range(int(Amount)):
                        productList.append(Productenter)
                else:
                    fullPrice += MyProducts[Productenter]
                    productList.append(Productenter)
                # add all values from the list to the listbox
    
            listbox.delete(0, END)  # clear listbox
            warenkorb = {}
            for i in productList:

                if i in warenkorb:
                    warenkorb[i] += 1
                else:
                    warenkorb[i] = 1

            for item in warenkorb:
                listbox.insert(END, item, str(MyProducts[item]) + "  x" + str( warenkorb[item] ))


            print(" Subtotal:  ", round(fullPrice, 2), " €" )
                
        except KeyError:
                print(f" {Fore.RED}This Product doesnt exist{Style.RESET_ALL}")
        except ValueError: 
                print(f" {Fore.RED}Something went wrong with the price/Amount{Style.RESET_ALL}")

def Delete():
    def on_submit():
        try:
            name = entry1.get()
            del MyProducts[name]
            np.save('my_file.npy', MyProducts)
            os.system('cls')
        except KeyError:
            print(f" {Fore.RED}This Product doesnt exist{Style.RESET_ALL}")
        window.destroy()
    window = tk.Tk()
    window.title("Value Entry")
    window.geometry("230x100")
    window.eval('tk::PlaceWindow . center')
    entry1 = tk.Entry(window)
    entry1.grid(row=0, column=1)

    tk.Label(window, text="Product").grid(row=0, column=0)

    submit_button = tk.Button(window, text="Bestätigen", command=on_submit)
    submit_button.grid(row=2, column=0, columnspan=2)

    window.mainloop()

import tkinter

import tkinter as tk

def restart_program():
    root.destroy()
    os.system(f"python {os.path.basename(sys.argv[0])}")
    sys.exit("Restart Script")


root = tkinter.Tk()
root.title("Example GUI")
root.attributes('-fullscreen', True)

# create listbox on left side
listbox = tkinter.Listbox(root, width=70)
listbox.pack(side=tkinter.LEFT, expand=False, fill=tkinter.Y)

button_frame = tkinter.Frame(root)
button_frame.pack(side='bottom')

create_button = tkinter.Button(button_frame, text="Create\nProduct", bg="green", command=Create)
create_button.pack(side="left" ,fill="x", padx=0, pady=5, expand=True)
create_button.configure(width=10, height=5)

delete_button = tkinter.Button(button_frame, text="Löschen", bg="red", command=Delete)
delete_button.pack(side="left" ,fill="x", padx=0, pady=5, expand=True)
delete_button.configure(width=10, height=5)

finish_button = tkinter.Button(button_frame, text="Fertig", bg="blue", command=finish)
finish_button.pack(side="left" ,fill="x", padx=0, pady=5, expand=True)
finish_button.configure(width=10, height=5)
restart_button = tkinter.Button(button_frame, text="Restart", bg="darkred", command=restart_program)
restart_button.pack(side="left" ,fill="x", padx=0, pady=5, expand=True)
restart_button.configure(width=10, height=5)

product_frame = tk.Frame(root)
product_frame.pack(side="top", anchor="ne", padx=10, pady=10)

def Productsbuttons():
    # Erstellen der Buttons und hinzufügen zum Frame
    num_columns = 10

    # Loop over the items and create a button for each item
    for i, item in enumerate(MyProducts):
        # Calculate the row and column for the button
        row = i // num_columns
        column = i % num_columns

        # Create the button and add it to the grid
        tk.Button(product_frame, text=str(item), bg="#ff5e5e", command=lambda item=item: ProductEnter(item, ""), width=10, height=5, wraplength=80).grid(row=row, column=column, padx=0, pady=0)
Productsbuttons()


root.mainloop()
