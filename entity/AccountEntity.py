import psycopg2
from utils.Config import Config

class AccountEntity:
    def __init__(self):
        self.dbname = "postgres"
        self.user = "postgres"
        self.host = "localhost"
        self.port = "5432"
        self.password = Config.DATABASE_PASSWORD

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Database Connection Established.")
        except Exception as error:
            print(f"Error connecting to the database: {error}")
            self.connection = None
            self.cursor = None

    def add_account(self, username, password, webSite):
        """Insert a new account into the accounts table."""
        try:
            if self.cursor:
                self.cursor.execute("INSERT INTO accounts (username, password, website) VALUES (%s, %s, %s)", (username, password, webSite))
                self.connection.commit()
                print(f"Account {username} added successfully.")
        except Exception as error:
            print(f"Error inserting account: {error}")

    def fetch_accounts(self):
        """Fetch all accounts from the accounts table."""
        try:
            if self.cursor:
                self.cursor.execute("SELECT * FROM accounts;")
                accounts = self.cursor.fetchall()
                return accounts
        except Exception as error:
            print(f"Error fetching accounts: {error}")
            return None

    def delete_account(self, account_id):
        """Delete an account by ID."""
        try:
            if self.cursor:
                self.cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
                account = self.cursor.fetchone()
                if account:
                    self.cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
                    self.connection.commit()
                    print(f"Account with ID {account_id} deleted successfully.")
                else:
                    print(f"Account with ID {account_id} not found. No deletion performed.")
        except Exception as error:
            print(f"Error deleting account: {error}")


    def fetch_account_by_website(self, website):
        """Fetch the username and password where the website matches."""
        try:
            self.cursor.execute("SELECT username, password FROM accounts WHERE LOWER(website) = LOWER(%s)", (website,))
            return self.cursor.fetchone()  # Returns one matching account
        except Exception as error:
            print(f"Error fetching account for website {website}: {error}")
            return None



    def reset_id_sequence(self):
        """Reset the account ID sequence to the next available value."""
        try:
            if self.cursor:
                self.cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM accounts")
                next_id = self.cursor.fetchone()[0]
                self.cursor.execute("ALTER SEQUENCE accounts_id_seq RESTART WITH %s", (next_id,))
                self.connection.commit()
                print(f"ID sequence reset to {next_id}.")
        except Exception as error:
            print(f"Error resetting ID sequence: {error}")

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database Connection closed.")
