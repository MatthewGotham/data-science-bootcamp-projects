# Create/open the database.
import sqlite3
from tabulate import tabulate
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()


# Create the table.
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    id int(4), 
    Title varchar(255), 
    Author varchar(255), 
    Qty int(3), 
    PRIMARY KEY (id)
    );''')
db.commit()


# Populate the table.
new_books = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30), 
(3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40), 
(3003, 'The Lion, The Witch and the Wardrobe', 'C.S. Lewis', 25), 
(3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37), 
(3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

#for book in new_books:
#    cursor.execute('''INSERT OR IGNORE INTO books(id, Title, Author, Qty) 
#    VALUES(?,?,?,?);''', book)
#    db.commit()


#####
# Functions:
# Add a book.
def add_book(title, author, quantity):
    
    # Automatically assign an ID number.
    cursor.execute("SELECT MAX(id) FROM books;")
    placeholder = cursor.fetchone()[0]
    if placeholder == None:
        new_id = 1000
    else:
        new_id = placeholder + 1 
    
    # Add the book.
    book_to_add = (new_id, title, author, quantity)
    cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
    VALUES(?,?,?,?)''', book_to_add)
    db.commit()
    
    # Reassurance
    print(
f'''{quantity} copies of '{title}' by {author} were added to the database, 
with ID number {new_id}.''')


# Output as table.
def output_table(sql_output):
    head = ("ID", "Title", "Author", "Quantity")
    print(tabulate(sql_output, headers = head))

#####


# User interface.
menu_string = '''
MAIN MENU
Please choose from the following options:
1. Enter book.
2. Update book.
3. Delete book.
4. Search books.
5. View entire inventory.
0. Exit.
'''

delete_string = '''
Please enter the ID number of the book you want to delete, or 0 to return to 
the main menu. You can search for book ID numbers from the main menu.
'''

update_string = '''
Please enter the ID number of the book you want to update, or 0 to return to 
the main menu. You can search for book ID numbers from the main menu.
'''

update_action = '''
Please choose from the following options:
T - Update the title.
A - Update the author.
Q - Update the quantity.
X - Exit without updating.
'''


# Options
while True:
    # Get the initial user selection.
    menu_choice = input(menu_string)

    # Exit.
    if menu_choice == '0':
        break

    # Add a book
    elif menu_choice == '1':
        new_title = input("What is the title of the book?\n")
        new_author = input(f"Who is the author of '{new_title}'?\n")

        test_quantity = input(f"How many copies of '{new_title}' do you want to add?\n")
        while not test_quantity.isnumeric():
            print("Please enter a valid (whole, positive) number of books.")
            test_quantity = input(f"How many copies of '{new_title}' do you want to add?\n")
        
        new_quantity = int(test_quantity)
        add_book(new_title, new_author, new_quantity)
        continue
                    
    
    # Update book.
    elif menu_choice == '2':
        # Get a list of valid ID numbers.
        cursor.execute("SELECT id FROM books;")
        ids = cursor.fetchall()
        ids = [str(id[0]) for id in ids]

        while True:
            to_update = input(update_string)
        
            if to_update == '0':
                break

            elif not to_update in ids:
                print("That is not a valid book ID number.\n")
                continue
        
            else:
                cursor.execute("SELECT * FROM books WHERE id = ?;", 
                [int(to_update)])
                row_to_update = cursor.fetchall()
                print("\n")
                output_table(row_to_update)
                
                while True:
                    update_type = input(update_action)

                    if update_type.lower() == 't':
                        # Update the title.
                        new_title = input("Enter the new title.\n")
                        cursor.execute("UPDATE books SET Title = ? WHERE id = ?;", 
                        (new_title, int(to_update)))
                        db.commit()
                        print("The title has been updated.")
                        break

                    elif update_type.lower() == 'a':
                        # Update the author.
                        new_author = input("Enter the new author.\n")
                        cursor.execute("UPDATE books SET Author = ? WHERE id = ?;", 
                        (new_author, int(to_update)))
                        db.commit()
                        print("The author has been updated.")
                        break

                    elif update_type.lower() == 'q':
                        # Update the quantity.
                        new_quantity = input("Enter the new quantity.\n")

                        while not new_quantity.isnumeric():
                            print("Please enter a valid (whole, positive) number of books.")
                            new_quantity = input("Enter the new quantity.\n")
                        
                        cursor.execute("UPDATE books SET Qty = ? WHERE id = ?;", 
                        (int(new_quantity), int(to_update)))
                        db.commit()
                        print("The quantity has been updated.")
                        
                        break

                    elif update_type.lower() == 'x':
                        print("No action has been taken.")
                        break

                    else:
                        print("I do not recognize that selection.")
                        continue

    
    # Delete book.
    elif menu_choice == '3':
        while True:
            # Get a list of valid ID numbers.
            cursor.execute("SELECT id FROM books;")
            ids = cursor.fetchall()
            ids = [str(id[0]) for id in ids]

            to_delete = input(delete_string)
        
            if to_delete == '0':
                break

            elif not to_delete in ids:
                print("That is not a valid book ID number.\n")
                continue
        
            else:
                cursor.execute("SELECT * FROM books WHERE id = ?;", 
                [int(to_delete)])
                row_to_delete = cursor.fetchall()
                print("\n")
                output_table(row_to_delete)
                
                while True:
                    deletion_confirmation = input(
                    "Are you sure you want to delete this book (y/n)?\n")

                    if deletion_confirmation.lower() == 'y':
                        cursor.execute("DELETE FROM books WHERE id = ?;", 
                        [int(to_delete)])
                        db.commit()
                        print("Record deleted.")
                        break

                    elif deletion_confirmation.lower() == 'n':
                        print("No action has been taken.")
                        break

                    else:
                        print("I do not recognize that selection.")
                        continue


    # Search books
    elif menu_choice == '4':
        search_string = input("Enter the title or author you want to search for.\n")
        search_string = f"%{search_string}%"
        cursor.execute("SELECT * FROM books WHERE Title LIKE ? OR Author LIKE ?;", 
        (search_string, search_string))
        results = cursor.fetchall()
        print("\nSearch results:")
        output_table(results)
        continue
    

    # View entire inventory.
    elif menu_choice == '5':
        cursor.execute("SELECT * FROM books;")
        output = cursor.fetchall()
        print("\nInventory:")
        output_table(output)
        continue
    

    else:
        # Inappropriate input
        print("I'm sorry, I don't recognize that choice.")
        continue