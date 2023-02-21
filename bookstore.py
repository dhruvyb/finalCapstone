import sqlite3, time, tabulate

# ID, title, author and quantity tuples defined for each of the existing books for database

book1 = (3001, "A Tale Of Two Cities", "Charles Dickens", 30)

book2 = (3002, "Harry Potter And The Philosopher\'s Stone", "J.K. Rowling", 40)

book3 = (3003, "The Lion, The Witch And The Wardrobe", "C.S. Lewis", 25)

book4 = (3004, "The Lord Of The Rings", "J.R.R. Tolkien", 37)

book5 = (3005, "Alice In Wonderland", "Lewis Carroll", 12)

# list of books created
books = [book1, book2, book3, book4, book5]

# database created for bookstore
db = sqlite3.connect('bookstore_db')

# cursor object created
cursor = db.cursor()

try:
    # try to select from table
    cursor.execute('''SELECT COUNT(bookstore.id) FROM bookstore''')

except:

    # create table if it does not already exist
    cursor.execute('''
        CREATE TABLE bookstore(
            id INTEGER PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(100),
            quantity INTEGER)''')

    # books added to table only if table did not previously exist
    cursor.executemany(''' 
        INSERT OR IGNORE INTO bookstore(id, title, author, quantity)
        VALUES(?,?,?,?)''', books)

    # commit to database
    db.commit()

def search_by_id():
    # search by id function

    # id to search made into global function
    global id_to_search


    while True:

        # enter id to search            
        id_to_search = input("\nEnter book ID:\n")

        # select book entry fields for id stated
        cursor.execute('''
            SELECT bookstore.id, bookstore.title, bookstore.author, bookstore.quantity
            FROM bookstore
            WHERE id = ?''', [id_to_search])
        
        # call book entry to list
        book_search = cursor.fetchall()
        
        # if list is empty, print book id not available
        if book_search == []:
            print("\nBook ID does not exist.")

        # else break
        else:
            break
    
    # print book entry using function
    print_books(book_search)

def search_by_title():
    # search by title function

    # title to search made into global function
    global title_to_search
    
    while True:
        # user to enter book title to search
        title_to_search = input("\nEnter book title:\n").title()

        # search table for title
        cursor.execute('''
            SELECT bookstore.id, bookstore.title, bookstore.author, bookstore.quantity
            FROM bookstore
            WHERE title = ?''', [title_to_search])
        book_search = cursor.fetchall()
        
        # if list empty, print title not available
        if book_search == []:
            print("\nBook Title does not exist in database.")

        else:
            # if more than one book with same title
            if len(book_search) > 1:

                # print selection of books
                print_books(book_search)

                # create list of ids with selected books               
                book_id_list = []
                for i in book_search:
                    book_id_list.append(str(i[0]))

                while True:
                    # ask user to select id from the selected books
                    id_to_search = input("\nSelect book ID from list:\n")

                    # if valid id chosen then break loop
                    if id_to_search in book_id_list:
                        break
                    else:
                        # if other id chosen, error message printed
                        print("\nInvalid Entry.\n")

                # select book using single id chosen
                cursor.execute('''
                    SELECT bookstore.id, bookstore.title, bookstore.author, bookstore.quantity
                    FROM bookstore
                    WHERE id = ?''', [id_to_search])
                book_search = cursor.fetchall()

            # print book details with function
            print_books(book_search)

        break
            
def search_by_author():
    # search by author function

    # author to search made into global function
    global author_to_search
    
    while True:
        # user to enter book author to search
        author_to_search = input("\nEnter book author:\n").title()

        # search table for author
        cursor.execute('''
            SELECT bookstore.id, bookstore.title, bookstore.author, bookstore.quantity
            FROM bookstore
            WHERE author = ?''', [author_to_search])
        book_search = cursor.fetchall()

        # if list empty, print author not available
        if book_search == []:
            print("\nAuthor does not exist in database.")

        else:
            # if more than one book with same author
            if len(book_search) > 1:

                # print selection of books
                print_books(book_search)

                # create list of ids with selected books  
                book_id_list = []
                for i in book_search:
                    book_id_list.append(str(i[0]))

                while True:
                    # ask user to select id from the selected books
                    id_to_search = input("\nSelect book ID from list:\n")

                    # if valid id chosen then break loop
                    if id_to_search in book_id_list:
                        break

                    else:
                        # if other id chosen, error message printed
                        print("\nInvalid Entry.\n")

                # select book using single id chosen            
                cursor.execute('''
                    SELECT bookstore.id, bookstore.title, bookstore.author, bookstore.quantity
                    FROM bookstore
                    WHERE id = ?''', [id_to_search])
                book_search = cursor.fetchall()

            # print book details with function
            print_books(book_search)
        break

def search_book():
    # search book function
    
        while True:
            # ask user to select method of search
            print('''
Select search method:
1   -   Search by ID
2   -   Search by Author
3   -   Search by Title''')

            # if search book option selected, print additional option
            if option == "4":
                print('''0   -   Return to Main Menu''')

            # ask user for selection
            search_option = input("\n")

            if search_option == "1":
                # search by id
                search_by_id()

                print("\n**Search Complete**\n")
                
                break

            elif search_option == "2":
                # search by author
                search_by_author()

                print("\n**Search Complete**\n")
                
                break                
                
            elif search_option == "3":
                # search by title
                search_by_title()

                print("\n**Search Complete**\n")
                
                break
                
            elif search_option == "0":
                
                # if Search Option was selected at main menu
                if option == "4":
                    # break out of search menu
                    break

                # else print invalid entry message
                else:
                    print("\nInvalid Entry. Please select from the options given.")
            
            # error message if wrong selection chosen
            else:
                print("\nInvalid Entry. Please select from the options given.")


def new_book():
    # function to enter new book to database

    print("\n**NEW BOOK**")

    # ask user for title and author
    new_title = input("\nEnter Title for new book:\n").title()

    new_author = input("\nEnter Author of new book:\n").title()

    # Checks combination of author and book title and selects from table and fetchone method called
    cursor.execute('''
        SELECT COUNT(bookstore.id) FROM bookstore
        WHERE title = ? AND author = ?''', (new_title, new_author))
    count = cursor.fetchone()

    # if book already exisit, prints statement to show this and function ends
    if count[0] == 1:
        print("\nBook already exists.")

    else:
        
        # if book title and author combination does not exist then ask user for quantity
        while True:
            try:
                new_qty = int(input("\nEnter Quantity of book:\n"))
            except ValueError:
                print("\nInvalid Entry. Enter a valid number.\n")
            finally:
                break
        
        # sets book id to 1 more than the max id value
        cursor.execute('''
            SELECT MAX(bookstore.id) FROM bookstore''')
        max_id = cursor.fetchone()[0]

        new_id = max_id + 1

        # insert book into table
        cursor.execute('''
            INSERT INTO bookstore
            VALUES(?,?,?,?)''', (new_id, new_title, new_author, new_qty))
        
        #commit changes
        db.commit()

        # print statement to confirm book has been added to table
        print(f'''
**New Book Added**

ID:         {new_id}
Title:      {new_title}
Author:     {new_author}
Quantity:   {new_qty}''')  

def print_books(book_list):
    # print books function
    
    if len(book_list) > 1:
    # if more than one book in list argument

        # code to create table from tabulate to display book entries
        header_all = ['ID', 'Title', 'Author']
        body_all = []
        for b in book_list:
            row = []
            for i in range(0, 3):
                row.append(b[i])
            body_all.append(row)
        
        # print table using tabulate
        print("\n" + tabulate.tabulate(body_all, headers=header_all, tablefmt="simple_outline"))

    else:
    # if 1 book in list argument, print book in format below
        print(f'''
ID:         {book_list[0][0]}
Title:      {book_list[0][1]}
Author:     {book_list[0][2]}
Quantity:   {book_list[0][3]}
''')
    

def update_book():
    # update book function
    
    # search book function called to select book to update
    search_by_id()

    # ask user for field to update
    update_option = input('''
Select field to update
a   -   Author
t   -   Title
q   -   Quantity

''').lower()

    if update_option == "a":
        # update author

        # update field with new author
        update_field = input("\nEnter new name for Author of book:\n").title()

        cursor.execute('''
            UPDATE bookstore
            SET author = ?
            WHERE id = ?''', (update_field, id_to_search))

    elif update_option == "t":
        # update title

        # update field with new title
        update_field = input("\nEnter new name for Title of book:\n").title()

        cursor.execute('''
            UPDATE bookstore
            SET title = ?
            WHERE id = ?''', (update_field, id_to_search))

    elif update_option == "q":
        #update quantity

        # while loop for integet entry validation
        while True:
            try:
                # ask user for new quantity of book
                update_field = int(input("\nEnter new quantity of book:\n"))
            
            # error message if integer not entered
            except ValueError:
                print("Invalid Entry.\n")
            else:
                break
        
        # update quantity of book in table
        cursor.execute('''
            UPDATE bookstore
            SET quantity = ?
            WHERE id = ?''', (update_field, id_to_search))
    else:
        print("\nInvalid Entry.")

    # commit changes to database
    db.commit()


option = ""
# while true loop to allow loop through menu after functions have run
while True:
    # while true block for main menu

    print("-" * 75)
    print("BOOKSTORE DATABASE")
    print("-" * 75)

    # ask user to select from options
    option = input('''
Select from the following options:

1   -   Enter New Book
2   -   Update Existing Book
3   -   Delete Book
4   -   Search Book
0   -   Exit

''')
  
    if option == "1":
        # new book entry option
        new_book()
        
        input("\nPress Enter to return to main menu.\n")

    elif option == "2":
        # update book entry option

        print("\n***UPDATE BOOK***")
        update_book()

        print("\n**Book Updated Successfully**")

        input("\nPress Enter to Return to Main Menu.\n")

    elif option == "3":
        # delete book option

        print("\n***Delete BOOK***")

        search_by_id()

        while True:

            # confirm deletion of book
            confirm_delete = input("\nAre you sure you want to delete this book from the database? (Y/N)\n").lower()
            if confirm_delete == "y":

                # delete book from table
                cursor.execute('''
                DELETE FROM bookstore
                WHERE id = ?''',(id_to_search,))

                # commit changes
                db.commit()

                print("**Book Deleted**")
                input("\nPress Enter to return to main menu.\n")
                break

            elif confirm_delete == "n":
                # Return to main menu without deleting
                input("\nPress Enter to return to main menu.\n")
                break
            
            else:
                print("Invalid Entry.")

    elif option == "4":
        # search book
        print("\n***SEARCH BOOK***")
        
        search_book()

        input("\nPress Enter to return to Main menu.\n")
        
    elif option == "0":
        
        # exit program
        print("Exiting Program...")
        print("Goodbye!")

        time.sleep(3)
        db.close()
        exit()
    
    else:
        # invalid option selected
        print("\nInvalid Entry. Please select from the options given.")


