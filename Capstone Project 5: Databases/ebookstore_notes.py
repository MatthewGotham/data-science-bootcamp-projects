# Create/open the database.
import sqlite3
from tabulate import tabulate
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()

# Create the table.

#cursor.execute("DROP TABLE IF EXISTS books;")
#db.commit()
# I decided not to do it this ^ way because I'd like to retain the table each time I run this.

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

for book in new_books:
    cursor.execute('''INSERT OR IGNORE INTO books(id, Title, Author, Qty) 
    VALUES(?,?,?,?);''', book)
    db.commit()


#####
# Functions:
# Add a book.
def add_book(title, author, quantity):
    
    # Automatically assign an ID number.
    cursor.execute("SELECT MAX(id) FROM books;")
    new_id = cursor.fetchone()[0] + 1 
    
    # Add the book.
    book_to_add = (new_id, title, author, quantity)
    cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
    VALUES(?,?,?,?)''', book_to_add)
    db.commit()
    
    # Reassurance
    print(
f'''{quantity} copies of '{title}' by {author} were added to the database, 
with ID number {new_id}.''')

# Update a book.
# Update the title.
def update_title(id, title):
    cursor.execute("UPDATE books SET Title = ? WHERE id = ?;", (title, id))
    db.commit()

# Update the author.
def update_author(id, author):
    cursor.execute("UPDATE books SET Author = ? WHERE id = ?;", (author, id))
    db.commit()

# Update the quantity.
def update_quantity(id, quantity):
    cursor.execute("UPDATE books SET Qty = ? WHERE id = ?;", (quantity, id))
    db.commit()

# Selecte update type.
def select_update():
    


# Output as table.
def output_table(sql_output):
    head = ("ID", "Title", "Author", "Quantity")
    print(tabulate(sql_output, headers = head))


#####
# User interface.
menu_string = '''MAIN MENU
Please choose from the following options:
1. Enter book.
2. Update book.
3. Delete book.
4. Search books.
5. View entire inventory.
0. Exit.
'''

# Get the initial user selection.
menu_choice = input(menu_string)


# Options
while menu_choice != '0': # Stay in the menu loop unless exit selected.
    # Inappropriate input
    if menu_choice not in [str(x) for x in range(6)]:
        print("I'm sorry, I don't recognize that choice.")
        menu_choice = input(menu_string)

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
        menu_choice = input(menu_string)
    
    # Update book.
    elif menu_choice == '2':
        cursor.execute("SELECT id FROM books;")
        ids = cursor.fetchall()
        ids = [str(id[0]) for id in ids]
        print(ids) # This is temporary.

        update_string = \
'''Enter the ID number of the book you want to update, or 0 to return to the
main menu. You can search for book ID numbers from the main menu.
'''
        update_selection = input(update_string)
        if update_selection == '0':
            menu_choice = input(menu_string)
        elif not update_selection in ids:
                print("That ID number is not recognized.")
                update_selection = input(update_string)
        else:
            cursor.execute("SELECT * FROM books WHERE id = ?;", [update_selection])
            selected = cursor.fetchall()
            output_table(selected)
            update_confirmation = input("Is this the book you mean to update (y/n)?")
            while update_confirmation.lower() not in ['y', 'n']:
                print("I do not recognize that selection.")
                output_table(selected)
                update_confirmation = input("Is this the book you mean to update (y/n)?")

            if update_confirmation.lower() == 'n':
                update_selection = input(update_string)
            elif update_confirmation.lower() == 'y':
                # do something
            else:
                


    
    # Search books
    elif menu_choice == '4':
        search_string = input("Enter the title or author you want to search for.\n")
        search_string = f"%{search_string}%"
        cursor.execute("SELECT * FROM books WHERE Title LIKE ? OR Author LIKE ?;", 
        (search_string, search_string))
        results = cursor.fetchall()
        print("\nSearch results:")
        output_table(results)
        print("\n")
        menu_choice = input(menu_string)
    
    # View entire inventory.
    elif menu_choice == '5':
        cursor.execute("SELECT * FROM books;")
        output = cursor.fetchall()
        print("\nInventory:")
        output_table(output)
        print("\n")
        menu_choice = input(menu_string)
    
    else:
        pass


# I want to see/check what this table looks like now.
#cursor.execute("SELECT * FROM books;")
#output = cursor.fetchall()
#print(output)

# Check for duplicates
# cursor.execute('''SELECT SUM(Qty) FROM books 
# WHERE Title = ? AND Author = ?''', (new_title, new_author))
# quant_already = cursor.fetchone()[0]