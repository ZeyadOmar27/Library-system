def add_click_book(book_listbox,book_entry,author_entry,fill_label):
    global books
    book = book_entry.get()
    author = author_entry.get()
    if book and author:
        for b in books:
            if book == b["book title"] and author == b["author"]:
                fill_label.config(text="Book already added", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
                fill_label.after(2000, lambda: fill_label.config(text=""))
            else:
                books.append({"book title": book, "author": author, "availability": "available"})
                book_listbox.insert(tk.END,"• "+ book + " - " + author)
                book_entry.delete(0, tk.END)
                author_entry.delete(0, tk.END)
                fill_label.config(text="Book added successfully", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
                fill_label.after(2000, lambda: fill_label.config(text=""))
    else:
        fill_label.config(text="Please fill in both book title and author", fg="#5C4033", font=("Arial", 13,"bold"), bg="#F5E1A4")
        fill_label.after(2000, lambda: fill_label.config(text=""))