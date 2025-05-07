import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import font
from PIL import Image, ImageTk #type: ignore


def main():
    draw()
    window.mainloop()

# Settings
ROWS = 35
COLUMNS = 20
TILE_SIZE = 25
WINDOW_HEIGHT = TILE_SIZE * COLUMNS
WINDOW_WIDTH = TILE_SIZE * ROWS

# Window
window = tk.Tk()
window.title("Library")
window.resizable(False, False)

# Canvas
canvas = tk.Canvas(window, bg="#F5E1A4", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=4, highlightthickness=0)
canvas.pack()
window.update()

# Center The Window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

books = []
members = []
borrowed_books = []
returned_books = []


#icon
window.iconbitmap("Assets/icon.ico")
#add_icon
add_icon = PhotoImage(file = "Assets/add.png")

#delete_icon
delete_icon = Image.open("Assets/delete.png")
delete = ImageTk.PhotoImage(delete_icon)
#edit_icon
edit_icon = Image.open("Assets/edit.png")
edit = ImageTk.PhotoImage(edit_icon)
#done_icon 
borrow_icon = Image.open("Assets/borrow.png")
borrow = ImageTk.PhotoImage(borrow_icon)
#undone_icon 
return_icon = Image.open("Assets/return.png")
return_ = ImageTk.PhotoImage(return_icon)
#search_icon
search_icon = Image.open("Assets/search.png")
search = ImageTk.PhotoImage(search_icon)



def show_selection(book_listbox):
    selected_index = book_listbox.curselection()
    if selected_index:
        book_listbox.config(selectbackground="#8B3A4A", selectforeground="black")  
        return selected_index[0]
    return None  

def show_selection_member(member_listbox):
    selected_index = member_listbox.curselection()
    if selected_index:
        member_listbox.config(selectbackground="#8B3A4A", selectforeground="black")  
        return selected_index[0]
    return None  
def add_click_book(book_listbox,book_entry,author_entry,fill_label):
    global books
    book = book_entry.get()
    author = author_entry.get()
    if book and author:
        for b in books:
            if book == b["book title"] and author == b["author"]:
                fill_label.config(text="Book already added", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
                fill_label.after(2000, lambda: fill_label.config(text=""))
                return

        books.append({"book title": book, "author": author, "availability": "available"})
        book_listbox.insert(tk.END,"• "+ book + " - " + author)
        book_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        fill_label.config(text="Book added successfully", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
        fill_label.after(2000, lambda: fill_label.config(text=""))
    else:
        fill_label.config(text="Please fill in both book title and author", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
        fill_label.after(2000, lambda: fill_label.config(text=""))


def add_click_member(member_listbox, member_entry, fill_label):
    global members
    member = member_entry.get()
    if member:
        members.append(member)
        member_listbox.insert(tk.END,"• "+ member)
        member_entry.delete(0, tk.END)
        fill_label.config(text="Member added successfully", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
        fill_label.after(2000, lambda: fill_label.config(text=""))
    else:
        fill_label.config(text="Please fill in member", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
        fill_label.after(2000, lambda: fill_label.config(text=""))

    
def delete_click(book_listbox, member_listbox, remove_label):
    selected_book_index = show_selection(book_listbox)
    selected_member_index = show_selection(member_listbox)
    if selected_book_index is not None:
        books.pop(selected_book_index)
        book_listbox.delete(selected_book_index)
        remove_label.config(text="Book removed successfully", fg="#5C4033", font=("Arial", 12,"bold"), bg="#F5E1A4")
        remove_label.after(2000, lambda: remove_label.config(text=""))

    elif selected_member_index is not None:
        members.pop(selected_member_index)
        member_listbox.delete(selected_member_index)
        remove_label.config(text="Member removed successfully", fg="#5C4033", font=("Arial", 12,"bold"), bg="#F5E1A4")
        remove_label.after(2000, lambda: remove_label.config(text=""))
    else:
        remove_label.config(text="Please select a book or a member to remove", fg="#5C4033", font=("Arial", 12,"bold"), bg="#F5E1A4")
        remove_label.after(2000, lambda: remove_label.config(text=""))

        


def borrow_click(book_listbox, member_listbox, borrow_label):
    selected_book_index = show_selection(book_listbox)
    selected_member_index = show_selection_member(member_listbox)

    if selected_book_index is not None and selected_member_index is not None:
        selected_book = books[selected_book_index]
        selected_member = members[selected_member_index]

        if selected_book["availability"] == "unavailable":
            borrow_label.config(text="This book is already borrowed!", fg="#5C4033", font=("Arial", 13, "bold"), bg="#F5E1A4")
            borrow_label.after(2000, lambda: borrow_label.config(text=""))
            return

        borrowed_books.append({"book": selected_book, "member": selected_member})

        book_listbox.delete(selected_book_index)
        book_listbox.insert(selected_book_index, f"• {selected_book['book title']} - {selected_book['author']} >>> [Not available] >>> borrowed by {selected_member}")
        books[selected_book_index]["availability"] = "unavailable"

        # Update the result label
        borrow_label.config(text=f"{selected_member} borrowed '{selected_book['book title']}'", fg="#5C4033", font=("Arial", 13, "bold"), bg="#F5E1A4")
        borrow_label.after(2000, lambda: borrow_label.config(text=""))  # Reset the result label after 2 seconds
    else:
        # Show error if either a book or member isn't selected
        borrow_label.config(text="Please select both a book and a member", fg="#5C4033", font=("Arial", 13, "bold"), bg="#F5E1A4")
        borrow_label.after(2000, lambda: borrow_label.config(text=""))



def return_click(book_listbox, member_listbox, return_label):
    selected_book_index = show_selection(book_listbox)
    selected_member_index = show_selection_member(member_listbox)

    if selected_book_index is not None and selected_member_index is not None:
        selected_book = books[selected_book_index]
        selected_member = members[selected_member_index]

        if selected_book["availability"] == "available":
            return_label.config(text="Error, Book is already returned.", fg="#5C4033", font=("Arial", 13, "bold"), bg="#F5E1A4")
            return_label.after(2000, lambda: return_label.config(text=""))
            return

        elif selected_book["availability"] == "unavailable" and any(entry["member"] == selected_member for entry in borrowed_books):
            book_listbox.delete(selected_book_index)
            book_listbox.insert(selected_book_index, f"• {selected_book['book title']} - {selected_book['author']}")
            books[selected_book_index]["availability"] = "available"
            return_label.config(text=f"{selected_member} returned '{selected_book['book title']}'", fg="#5C4033", font=("Arial", 13, "bold"), bg="#F5E1A4")
            return_label.after(2000, lambda: return_label.config(text="")) 
            for entry in borrowed_books:
                if entry["member"] == selected_member and entry["book"] == selected_book:
                    borrowed_books.remove(entry)
                    break
    else:
        
        return_label.config(text="Please select both a book and a member", fg="#5C4033", font=("Arial", 13, "bold"), bg="#F5E1A4")
        return_label.after(2000, lambda: return_label.config(text=""))

def edit_click(book_listbox, book_entry, author_entry, edit_label):
    global books
    selected_index = show_selection(book_listbox)
    book = book_entry.get()
    author = author_entry.get()
    if selected_index is not None:
        if book and author:
            book_listbox.delete(selected_index)
            book_listbox.insert(selected_index, "• " + book + " - " + author)
            books[selected_index]["book title"] = book
            books[selected_index]["author"] = author

        elif book:
            book_listbox.delete(selected_index)
            book_listbox.insert(selected_index, "• " + book + " - " + books[selected_index]["author"])
            books[selected_index]["book title"] = book

        elif author:
            book_listbox.delete(selected_index)
            book_listbox.insert(selected_index, "• " + books[selected_index]["book title"] + " - " + author)
            books[selected_index]["author"] = author
            


    else:
        edit_label.config(text="Please select a book or a member to edit it's details", fg="#5C4033", font=("Arial", 10,"bold"), bg="#F5E1A4")
        edit_label.after(2000, lambda: edit_label.config(text=""))

    book_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)

def search_click(book_entry, author_entry, book_listbox, member_listbox, member_entry, result_label):
    global books, members

    book_listbox.delete(0, tk.END)
    member_listbox.delete(0, tk.END)

    matches_books = []
    matches_members = []

    book = book_entry.get().strip().lower()
    author = author_entry.get().strip().lower()
    member = member_entry.get().strip().lower()


    if book or author:
        for b in books:
            book_saved = b["book title"].lower()
            author_saved = b["author"].lower()

            if book == book_saved or author == author_saved:
                status = b.get("availability", "available")

                borrowed_by = None
                for entry in borrowed_books:
                    if (entry["book"]["book title"] == b["book title"] and
                        entry["book"]["author"] == b["author"]):
                        borrowed_by = entry["member"]
                        break

                if status == "unavailable" and borrowed_by:
                    display_text = f"• {b['book title']} - {b['author']} >>> [Not available] >>> borrowed by {borrowed_by}"
                else:
                    display_text = f"• {b['book title']} - {b['author']}"

                matches_books.append(display_text)


    if not book and not author:
        for b in books:
            status = b.get("availability", "available")

            borrowed_by = None
            for entry in borrowed_books:
                if (entry["book"]["book title"] == b["book title"] and
                    entry["book"]["author"] == b["author"]):
                    borrowed_by = entry["member"]
                    break

            if status == "unavailable" and borrowed_by:
                display_text = f"• {b['book title']} - {b['author']} >>> [Not available] >>> borrowed by {borrowed_by}"
            else:
                display_text = f"• {b['book title']} - {b['author']}"

            matches_books.append(display_text)

 
    if member:
        for m in members:
            if member in m.lower():
                matches_members.append(f"• {m}")
    else:
        for m in members:
            matches_members.append(f"• {m}")


    for match in matches_books:
        book_listbox.insert(tk.END, match)

    for match in matches_members:
        member_listbox.insert(tk.END, match)

 
    if not matches_books and not matches_members:
        result_label.config(text="No Matches Found", fg="#5C4033", font=("Arial", 20, "bold"), bg="#F5E1A4")
    else:
        result_label.config(text="Matches Found", fg="#5C4033", font=("Arial", 20, "bold"), bg="#F5E1A4")

    result_label.after(2000, lambda: result_label.config(text=""))




def draw():
    canvas.create_text(440, 49, text="⁃⁃⁃Library ⁃⁃⁃", font=("Great Vibes", 50,"bold"), fill="#8B3A4A")
    canvas.create_line(0, 90, 880, 90, fill="#8B3A4A", width=3)
    canvas.create_line(5, 90, 5, 505, fill="#8B3A4A", width=3)
    canvas.create_line(502, 90, 502, 439, fill="#8B3A4A", width=3)
    canvas.create_line(0, 502, 880, 502, fill="#8B3A4A", width=3)
    canvas.create_line(0, 165, 880, 165, fill="#8B3A4A", width=3)
    canvas.create_line(0, 440, 880, 440, fill="#8B3A4A", width=3)
    canvas.create_line(212, 90, 212, 165, fill="#8B3A4A", width=3)
    canvas.create_line(432, 90, 432, 165, fill="#8B3A4A", width=3)
    canvas.create_line(877, 89, 877, 505, fill="#8B3A4A", width=3)
    canvas.create_line(752, 90, 752, 165, fill="#8B3A4A", width=3)
    canvas.create_line(390, 440, 390, 539, fill="#8B3A4A", width=3)

    canvas.create_text(110, 110, text="Book", font=("comic sans", 20,"bold"), fill="#8B3A4A")
    canvas.create_text(325, 110, text="Author", font=("comic sans", 20,"bold"), fill="#8B3A4A")
    canvas.create_text(625, 110, text="Member", font=("comic sans", 20,"bold"), fill="#8B3A4A")
    canvas.create_text(250, 188, text="✤Books✤", font=("ariel", 20, "bold"), fill="#8B3A4A")
    canvas.create_line(190, 202, 310, 202, fill="#8B3A4A", width=2)
    canvas.create_text(690, 188, text="✤Members✤", font=("ariel", 20, "bold"), fill="#8B3A4A")
    canvas.create_line(609, 202, 770, 202, fill="#8B3A4A", width=2)
    canvas.create_text(460, 473, text="Activity:", font=("comic sans", 20,"bold"), fill="#8B3A4A")
    canvas.create_line(405, 488, 515, 488, fill="#8B3A4A", width=2)

    canvas.create_line(190, 124, 190, 156, fill="#8B3A4A", width=3)
    canvas.create_line(26, 123, 192, 123, fill="#8B3A4A", width=3)
    canvas.create_line(26.5, 124, 26.5, 156, fill="#8B3A4A", width=3)
    canvas.create_line(26, 156, 192, 156, fill="#8B3A4A", width=3)

    canvas.create_line(403, 124, 403, 156, fill="#8B3A4A", width=3)
    canvas.create_line(239, 123, 405, 123, fill="#8B3A4A", width=3)
    canvas.create_line(240, 124, 240, 156, fill="#8B3A4A", width=3)
    canvas.create_line(239, 156, 405, 156, fill="#8B3A4A", width=3)

    canvas.create_line(703, 124, 703, 156, fill="#8B3A4A", width=3)
    canvas.create_line(539, 123, 705, 123, fill="#8B3A4A", width=3)
    canvas.create_line(540, 124, 540, 156, fill="#8B3A4A", width=3)
    canvas.create_line(539, 156, 705, 156, fill="#8B3A4A", width=3)
    

    add_button = tk.Button(window, image=add_icon, bg="#F5E1A4", bd=0, relief="flat",  activebackground="#F5E1A4", highlightthickness=0, command=lambda: add_click_book(book_listbox, book, author, fill_label))
    add_button.place(x=443, y=103)

    add_member_button = tk.Button(window, image=add_icon, bg="#F5E1A4", bd=0, relief="flat",  activebackground="#F5E1A4", highlightthickness=0, command=lambda: add_click_member(member_listbox, member, fill_label))
    add_member_button.place(x=790, y=103)

    book = tk.Entry(window, font=("Ariel", 15, "bold"), bg="#F5E1A4", fg="#8B3A4A", justify="center",insertbackground="#8B3A4A",  bd=0)
    book.place(x=29 , y=125 , width=160, height=30)

    author = tk.Entry(window, font=("Ariel", 15, "bold"), bg="#F5E1A4", fg="#8B3A4A", justify="center",insertbackground="#8B3A4A",  bd=0)
    author.place(x=242 , y=125 , width=160, height=30)

    member = tk.Entry(window, font=("Ariel", 15, "bold"), bg="#F5E1A4", fg="#8B3A4A", justify="center",insertbackground="#8B3A4A",  bd=0)
    member.place(x=542 , y=125 , width=160, height=30)

    

    delete_button = tk.Button(window, image=delete, bg="#F5E1A4", bd=0, relief="flat",  activebackground="#F5E1A4", highlightthickness=0, command=lambda: delete_click(book_listbox, member_listbox, remove_label))
    delete_button.place(x=248, y=450)

    edit_button = tk.Button(window, image=edit, bg="#F5E1A4", bd=0, relief="flat",  activebackground="#F5E1A4", highlightthickness=0, command=lambda: edit_click(book_listbox, book, author, edit_label))
    edit_button.place(x=170, y=450)  

    borrow_button = tk.Button(window, image=borrow, bg="#F5E1A4", bd=0, relief="flat",  activebackground="#F5E1A4", highlightthickness=0, command=lambda: borrow_click(book_listbox, member_listbox, borrow_label))
    borrow_button.place(x=10, y=450)   

    return_button = tk.Button(window, image=return_, bg="#F5E1A4", bd=0, relief="flat",  activebackground="#F5E1A4", highlightthickness=0, command=lambda: return_click(book_listbox, member_listbox, return_label))
    return_button.place(x=90, y=450) 

    search_button = tk.Button(window, image=search, bg="#F5E1A4", bd=0, relief="flat",  activebackground="#F5E1A4", highlightthickness=0, command=lambda: search_click(book, author, book_listbox, member_listbox, member, result_label))
    search_button.place(x=318, y=450)  

    book_listbox = tk.Listbox(window, height=15, width=80, bg="#F5E1A4",highlightthickness=0, fg="#8B3A4A", font=("comic sans", 8,"bold"), relief="flat", exportselection=0)
    book_listbox.place(x=12 , y=210)

    book_listbox.bind("<<ListboxSelect>>", lambda event: show_selection(book_listbox))

    member_listbox = tk.Listbox(window, height=15, width=60, bg="#F5E1A4",highlightthickness=0, fg="#8B3A4A", font=("comic sans", 8,"bold"), relief="flat", exportselection=0)
    member_listbox.place(x=510 , y=210)

    member_listbox.bind("<<ListboxSelect>>", lambda event: show_selection(member_listbox))

    result_label = tk.Label(window, text="", fg="#8B3A4A", font=("Arial", 6), bg="#F5E1A4", justify="center")
    result_label.place(x=550, y=455)

    fill_label = tk.Label(window, text="", fg="#8B3A4A", font=("Arial", 6), bg="#F5E1A4", justify="center")
    fill_label.place(x=540, y=462)

    edit_label = tk.Label(window, text="", fg="#8B3A4A", font=("Arial", 6), bg="#F5E1A4", justify="center")
    edit_label.place(x=538, y=462)

    remove_label = tk.Label(window, text="", fg="#8B3A4A", font=("Arial", 6), bg="#F5E1A4", justify="center")
    remove_label.place(x=535, y=462)

    borrow_label = tk.Label(window, text="", fg="#8B3A4A", font=("Arial", 6), bg="#F5E1A4", justify="center")
    borrow_label.place(x=533, y=462)

    return_label = tk.Label(window, text="", fg="#8B3A4A", font=("Arial", 6), bg="#F5E1A4", justify="center")
    return_label.place(x=530, y=462)

    #Create vertical scrollbar

    def on_mouse_wheel(event):
        book_listbox.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind the mouse wheel event to the book_listbox
        book_listbox.bind_all("<MouseWheel>", on_mouse_wheel)
    
    show_selection(book_listbox)

if __name__ == "__main__":
    main()

