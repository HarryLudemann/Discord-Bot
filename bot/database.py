import logging 
import psycopg2
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    from bot.database import Database

class Database:
    CHECK_USER_QUERY = lambda _, user_id, guild_id: f"SELECT * FROM users WHERE user_id = {user_id} AND guild_id = {guild_id}"
    GET_BALANCE_QUERY = lambda _, user_id, guild_id: f"SELECT balance FROM users WHERE user_id = {user_id} AND guild_id = {guild_id}"
    CREATE_USER_QUERY = lambda _, user_id, guild_id: f"INSERT INTO users (user_id, guild_id, balance) VALUES ({user_id}, {guild_id}, 0)"

    def list_to_string(list: list, line_addition='', uppercase_first=False) -> str:
        """Convert a list to a string"""
        string = ''
        for item in list:
            if uppercase_first:
                string += f'{item[0].upper()}{item[1:]}{line_addition}'
            else:
                string += f'{item}{line_addition}'
        return string

    def connect(self):
        """ Connect to local MySQL database, check db exits"""
        try:
            load_dotenv()
            conn = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST'),
                database=os.getenv('POSTGRES_DATABASE'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD')
            )
            # user table with balance and user id
            user_table_query = """CREATE TABLE IF NOT EXISTS users (
                guild_id bigserial PRIMARY KEY,
                user_id bigserial,
                balance INTEGER
            )"""
            # banned words table with random id and guild_id and word 
            banned_word_table_query = """CREATE TABLE IF NOT EXISTS banned_words (
                id bigserial PRIMARY KEY,
                guild_id bigserial,
                word VARCHAR(255)
            )"""
            # reaction roles table with guild_id , channel_id , role_id, and emoji
            reaction_roles_table_query = """CREATE TABLE IF NOT EXISTS reaction_roles (
                id bigserial PRIMARY KEY,
                guild_id bigserial,
                channel_id bigserial,
                role_id bigserial,
                emoji VARCHAR(255)
            )"""
            # prefix table with guild_id and prefix
            prefix_table_query = """CREATE TABLE IF NOT EXISTS prefixes (
                id bigserial PRIMARY KEY,
                guild_id bigserial,
                prefix VARCHAR(255)
            )"""
            cursor = conn.cursor()
            cursor.execute(user_table_query)
            cursor.execute(banned_word_table_query)
            cursor.execute(reaction_roles_table_query)
            cursor.execute(prefix_table_query)
            conn.commit()
            cursor.close()
            if conn is not None:
                logging.info('Connected to database')
            else:
                logging.error('Failed to connect to database')
            return conn
        except Exception as e:
            logging.error(e)
    
    def create_user(self, guild_id: str, user_id: str, conn = None) -> bool:
        """Create user if not exists, return True if created, False if already exists"""
        if conn is None:
            conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(user_id, guild_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(user_id, guild_id))
                conn.commit()
                return True
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()


class PrefixDatabase(Database):
    CHECK_PREFIX_QUERY = lambda _, guild_id: f"SELECT * FROM prefixes WHERE guild_id = {guild_id}"
    
    def create_def_prefix(self, guild_id: str) -> bool:
        """Create default prefix if not exists, return True if created, False if already exists"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_PREFIX_QUERY(guild_id))
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO prefixes (guild_id, prefix) VALUES ({guild_id}, '#')")
                conn.commit()
                return True
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    async def get_prefix(self, guild_id: str) -> str:
        """Get prefix, return None if not found"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            # check if prefix exists
            cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {guild_id}")
            if cursor.fetchone() is None:
                self.create_def_prefix(guild_id)
                return '#'
            cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {guild_id}")
            prefix = cursor.fetchone()
            if prefix is None:
                return None
            return prefix[0]
        except Exception as e:
            logging.error(e)
            return None
        finally:
            cursor.close()
            conn.close()

    def set_prefix(self, guild_id: str, prefix: str) -> bool:
        """Set prefix, return True if successful, False if not"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {guild_id}")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO prefixes (guild_id, prefix) VALUES ({guild_id}, '{prefix}')")
            else:
                cursor.execute(f"UPDATE prefixes SET prefix = '{prefix}' WHERE guild_id = {guild_id}")
            conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()


class BankDatabase(Database):
    def pay_user(self, guild_id: str, sender_id: str, recipient_id: str, amount: str, conn = None) -> bool:
        """Pay user, return True if successful, False if not. Checks if user exists"""
        conn = self.connect()
        if conn is None:
            logging.error("Failed to connect to database to pay user")
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(sender_id, guild_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(sender_id, guild_id))
                conn.commit()
            cursor.execute(self.CHECK_USER_QUERY(recipient_id, guild_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(recipient_id, guild_id))
                conn.commit()
            cursor.execute(self.GET_BALANCE_QUERY(sender_id, guild_id))
            sender_balance = cursor.fetchone()[0]
            if sender_balance < int(amount):
                return False
            cursor.execute(f"UPDATE users SET balance = balance - {amount} WHERE user_id = {sender_id} AND guild_id = {guild_id}")
            cursor.execute(f"UPDATE users SET balance = balance + {amount} WHERE user_id = {recipient_id} AND guild_id = {guild_id}")
            conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def set_user_balance(self, guild_id: str, user_id: str, amount: str, conn = None) -> bool:
        """Set user balance, return True if successful, False if not. Checks if user exists"""
        conn = self.connect()
        if conn is None:
            logging.error("Failed to connect to database to set user balance")
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(user_id, guild_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(user_id, guild_id))
                conn.commit()
            cursor.execute(f"UPDATE users SET balance = {amount} WHERE user_id = {user_id} AND guild_id = {guild_id}")
            conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user_balance(self, guild_id: str, user_id: str) -> int:
        """Get user balance, return balance if successful, None if not. Checks if user exists"""
        conn = self.connect()
        if conn is None:
            logging.error("Failed to connect to database to get user balance")
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(self.CHECK_USER_QUERY(user_id, guild_id))
            if cursor.fetchone() is None:
                cursor.execute(self.CREATE_USER_QUERY(user_id, guild_id))
                conn.commit()
            cursor.execute(self.GET_BALANCE_QUERY(user_id, guild_id))
            balance = cursor.fetchone()[0]
            return balance
        except Exception as e:
            logging.error(e)
            return None
        finally:
            cursor.close()
            conn.close()

class BannedWordsDatabase(Database):
    CHECK_WORD_QUERY = lambda _, word, guild_id: f"SELECT * FROM banned_words WHERE word = '{word}' AND guild_id = {guild_id}"

    def add_word(self, guild_id: str, word: str) -> bool:
        """Add word to banned_words table, return True if successful, False if not"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            word = word.lower()
            cursor.execute(self.CHECK_WORD_QUERY(word, guild_id))
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO banned_words (guild_id, word) VALUES ({guild_id}, '{word}')")
                conn.commit()
                return True
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def remove_word(self, guild_id: str, word: str, conn = None) -> bool:
        """Remove word from banned_words table, return True if successful, False if not"""
        if conn is None:
            conn = self.connect()
        cursor = conn.cursor()
        try:
            word = word.lower()
            cursor.execute(self.CHECK_WORD_QUERY(word, guild_id))
            if cursor.fetchone() is not None:
                cursor.execute(f"DELETE FROM banned_words WHERE word = '{word}' AND guild_id = {guild_id}")
                conn.commit()
                return True
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def get_words(self, guild_id: str) -> list:
        """Get all words from banned_words table, return list of words"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT word FROM banned_words WHERE guild_id = {guild_id}")
            words = cursor.fetchall()
            for i in range(len(words)):
                words[i] = words[i][0]
            return words
        except Exception as e:
            logging.error(e)
            return None
        finally:
            cursor.close()
            conn.close()

    def check_message(self, guild_id: str, message: str) -> bool:
        """Check message for banned words, return True if message contains banned words, False if not"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            message = message.lower()
            cursor.execute(f"SELECT word FROM banned_words WHERE guild_id = {guild_id}")
            words = cursor.fetchall()
            for word in words:
                if word[0] in message:
                    return True
            return False
        except Exception as e:
            logging.error(e)
            return None
        finally:
            cursor.close()
            conn.close()


class ReactionRoleDatabase(Database):

    def add_reaction_role(self, guild_id: str, channel_id: str, role_id: str, emoji: str) -> bool:
        """Add reaction role to reaction_roles table, return True if successful, False if not"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(f"INSERT INTO reaction_roles (guild_id, channel_id, role_id, emoji) VALUES ({guild_id}, {channel_id}, {role_id}, '{emoji}')")
            conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def remove_reaction_role(self, guild_id: str, channel_id: str, role_id: str, emoji: str) -> bool:
        """Remove reaction role from reaction_roles table, return True if successful, False if not"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM reaction_roles WHERE guild_id = {guild_id} AND channel_id = {channel_id} AND role_id = {role_id} AND emoji = '{emoji}'")
            conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def get_reaction_roles(self, guild_id: str) -> list:
        """Get all reaction roles from reaction_roles table, return list of reaction roles"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT role_id, emoji FROM reaction_roles WHERE guild_id = {guild_id}")
            reaction_roles = cursor.fetchall()
            return reaction_roles
        except Exception as e:
            logging.error(e)
            return []
        finally:
            cursor.close()
            conn.close()

    def check_reaction_role(self, guild_id: str, channel_id: str, emoji: str) -> str:
        """Check if reaction role exists, return role_id if successful, None if not"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT role_id FROM reaction_roles WHERE guild_id = {guild_id} AND channel_id = {channel_id} AND emoji = '{emoji}'")
            role_id = cursor.fetchone()
            if role_id is None:
                return None
            return role_id[0]
        except Exception as e:
            logging.error(e)
            return None
        finally:
            cursor.close()
            conn.close()



