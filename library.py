import sqlite3
from datetime import datetime

def initialize_database():
    """Create the database and members table if it doesn't exist"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            membership_date TEXT,
            status TEXT DEFAULT 'Active'
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def main_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("      LIBRARY MEMBER MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add New Member")
    print("2. View All Members")
    print("3. Search Member")
    print("4. Update Member")
    print("5. Delete Member")
    print("6. Exit")
    print("="*50)

def add_member():
    """Add a new member to the database"""
    print("\n--- ADD NEW MEMBER ---")
    
    try:
        name = input("Enter member name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        
        # Get current date for membership
        membership_date = datetime.now().strftime("%Y-%m-%d")
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO members (name, email, phone, membership_date)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, membership_date))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Member '{name}' added successfully!")
        
    except sqlite3.IntegrityError:
        print("❌ Error: Email already exists!")
    except Exception as e:
        print(f"❌ Error: {e}")

def view_all_members():
    """Display all members"""
    print("\n--- ALL LIBRARY MEMBERS ---")
    
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    
    conn.close()
    
    if not members:
        print("No members found in the database.")
        return
    
    print(f"\n{'ID':<5} {'Name':<20} {'Email':<25} {'Phone':<15} {'Status':<10} {'Join Date':<12}")
    print("-" * 95)
    
    for member in members:
        member_id, name, email, phone, join_date, status = member
        print(f"{member_id:<5} {name:<20} {email:<25} {phone:<15} {status:<10} {join_date:<12}")

def search_member():
    """Search for a member by ID or name"""
    print("\n--- SEARCH MEMBER ---")
    print("1. Search by ID")
    print("2. Search by Name")
    
    choice = input("Choose search method (1-2): ")
    
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    if choice == '1':
        try:
            member_id = int(input("Enter member ID: "))
            cursor.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
        except ValueError:
            print("❌ Please enter a valid number!")
            return
    elif choice == '2':
        name = input("Enter member name: ")
        cursor.execute('SELECT * FROM members WHERE name LIKE ?', (f'%{name}%',))
    else:
        print("❌ Invalid choice!")
        return
    
    members = cursor.fetchall()
    conn.close()
    
    if not members:
        print("❌ No members found matching your criteria.")
        return
    
    print(f"\n{'ID':<5} {'Name':<20} {'Email':<25} {'Phone':<15} {'Status':<10} {'Join Date':<12}")
    print("-" * 95)
    
    for member in members:
        member_id, name, email, phone, join_date, status = member
        print(f"{member_id:<5} {name:<20} {email:<25} {phone:<15} {status:<10} {join_date:<12}")

def update_member():
    """Update member information"""
    print("\n--- UPDATE MEMBER ---")
    
    try:
        member_id = int(input("Enter member ID to update: "))
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Check if member exists
        cursor.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
        member = cursor.fetchone()
        
        if not member:
            print("❌ Member not found!")
            conn.close()
            return
        
        print(f"\nCurrent details for Member ID {member_id}:")
        print(f"Name: {member[1]}")
        print(f"Email: {member[2]}")
        print(f"Phone: {member[3]}")
        print(f"Status: {member[5]}")
        
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Email")
        print("3. Phone")
        print("4. Status")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            new_name = input("Enter new name: ")
            cursor.execute('UPDATE members SET name = ? WHERE member_id = ?', (new_name, member_id))
        elif choice == '2':
            new_email = input("Enter new email: ")
            cursor.execute('UPDATE members SET email = ? WHERE member_id = ?', (new_email, member_id))
        elif choice == '3':
            new_phone = input("Enter new phone: ")
            cursor.execute('UPDATE members SET phone = ? WHERE member_id = ?', (new_phone, member_id))
        elif choice == '4':
            new_status = input("Enter new status (Active/Inactive): ")
            cursor.execute('UPDATE members SET status = ? WHERE member_id = ?', (new_status, member_id))
        else:
            print("❌ Invalid choice!")
            conn.close()
            return
        
        conn.commit()
        conn.close()
        print("✅ Member updated successfully!")
        
    except ValueError:
        print("❌ Please enter a valid member ID!")
    except Exception as e:
        print(f"❌ Error: {e}")

def delete_member():
    """Delete a member from the database"""
    print("\n--- DELETE MEMBER ---")
    
    try:
        member_id = int(input("Enter member ID to delete: "))
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Check if member exists
        cursor.execute('SELECT name FROM members WHERE member_id = ?', (member_id,))
        member = cursor.fetchone()
        
        if not member:
            print("❌ Member not found!")
            conn.close()
            return
        
        confirm = input(f"Are you sure you want to delete member '{member[0]}'? (y/n): ")
        
        if confirm.lower() == 'y':
            cursor.execute('DELETE FROM members WHERE member_id = ?', (member_id,))
            conn.commit()
            print("✅ Member deleted successfully!")
        else:
            print("❌ Deletion cancelled.")
        
        conn.close()
        
    except ValueError:
        print("❌ Please enter a valid member ID!")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main program loop"""
    # Initialize database
    initialize_database()
    
    while True:
        # Show the menu first
        main_menu()
        
        # THEN ask for choice
        choice = input("\nENTER YOUR CHOICE (1-6): ")
        
        # Based on choice, call the appropriate function
        if choice == '1':
            add_member()
        elif choice == '2':
            view_all_members()
        elif choice == '3':
            search_member()
        elif choice == '4':
            update_member()
        elif choice == '5':
            delete_member()
        elif choice == '6':
            print("\nThank you for using Library Management System! 👋")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1-6.")
        
        # Wait for user to press Enter before showing menu again
        input("\nPress Enter to continue...")

# Start the program
if __name__ == "__main__":
    main()