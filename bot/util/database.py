import logging 
import psycopg2

if __name__ == "__main__":
    from bot.util.database import Database
    from bot.constants import POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST


class Database:
    CHECK_USER_QUERY = lambda user_id: f"SELECT * FROM users WHERE id = {user_id}"
    GET_BALANCE_QUERY = lambda user_id: f"SELECT balance FROM users WHERE id = {user_id}"
    CREATE_USER_QUERY = lambda user_id: f"INSERT INTO users (id, balance) VALUES ({user_id}, 0)"

    def connect(self):
        """ Connect to local MySQL database, check db exits"""
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                database=POSTGRES_DATABASE,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            # create user table if doesn't exists
            query = """CREATE TABLE IF NOT EXISTS users (
                id bigserial PRIMARY KEY,
                balance INTEGER
            )"""
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            return conn
        except Exception as e:
            logging.error(e)
    
    def create_user(self, user_id: str, conn = None) -> bool:
        """Create user if not exists, return True if created, False if already exists"""
        if conn is None:
            conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(user_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(user_id))
                conn.commit()
                return True
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()


class BankDatabase(Database):
    def pay_user(self, sender_id: str, recipient_id: str, amount: str, conn = None) -> bool:
        """Pay user, return True if successful, False if not"""
        if conn is None:
            conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(sender_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(sender_id))
                conn.commit()
            cursor.execute(self.CHECK_USER_QUERY(recipient_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(recipient_id))
                conn.commit()
            cursor.execute(self.GET_BALANCE_QUERY(sender_id))
            sender_balance = cursor.fetchone()[0]
            if sender_balance < int(amount):
                return False
            cursor.execute(f"UPDATE users SET balance = balance - {amount} WHERE id = {sender_id}")
            cursor.execute(f"UPDATE users SET balance = balance + {amount} WHERE id = {recipient_id}")
            conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def set_user_balance(self, user_id: str, amount: str, conn = None) -> bool:
        """Set user balance, return True if successful, False if not"""
        if conn is None:
            conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(user_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(user_id))
                conn.commit()
            cursor.execute(f"UPDATE users SET balance = {amount} WHERE id = {user_id}")
            conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user_balance(self, user_id: str, conn = None) -> int:
        if conn is None:
            conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(user_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(user_id))
                conn.commit()
            cursor.execute(self.GET_BALANCE_QUERY(user_id))
            balance = cursor.fetchone()[0]
            return balance
        except Exception as e:
            logging.error(e)
            return None
        finally:
            cursor.close()
            conn.close()
