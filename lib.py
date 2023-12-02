import sqlite3
import json

def read_credentials(file_path: str) -> list:
    """
    Read credentials from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing credentials.

    Returns:
        list: List of dictionaries containing username and password pairs.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            credentials = json.load(file)
        return credentials
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading credentials file: {e}")
        return []

def create_database_and_table():
    """
    Create SQLite database and 'members' table.
    """
    try:
        conn = sqlite3.connect("wanghong.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                iid INTEGER PRIMARY KEY AUTOINCREMENT,
                mname TEXT NOT NULL,
                msex TEXT NOT NULL,
                mphone TEXT NOT NULL
            )
        """)

        conn.commit()
        print("=>資料庫已建立")
    except sqlite3.Error as e:
        print(f"Error creating database and table: {e}")
    finally:
        conn.close()

def import_data_from_file(file_path: str):
    """
    Import data from a file and insert into 'members' table.

    Args:
        file_path (str): Path to the data file.
    """
    try:
        conn = sqlite3.connect("wanghong.db")
        cursor = conn.cursor()

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(',')
                mname, msex, mphone = data
                cursor.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)", (mname, msex, mphone))

        conn.commit()
        print(f"=>異動 {conn.total_changes} 筆記錄")
    except (sqlite3.Error, FileNotFoundError) as e:
        print("=>查無資料")
    finally:
        conn.close()

def display_menu():
    """
    Display the menu options.
    """
    print("""
---------- 選單 ----------
0 / Enter 離開
1 建立資料庫與資料表
2 匯入資料
3 顯示所有紀錄
4 新增記錄
5 修改記錄
6 查詢指定手機
7 刪除所有記錄
--------------------------
    """)

def show_all_records():
    """
    Display all records from 'members' table.
    """
    try:
        conn = sqlite3.connect("wanghong.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM members")
        records = cursor.fetchall()

        if not records:
            print("=>查無資料")
        else:
            print("姓名　　　　性別　手機\n" + "-" * 29)
            for record in records:
                print(f"{record[1]:<8}　{record[2]:<2}　{record[3]:<12}")

    except sqlite3.Error as e:
        print("=>查無資料")
    finally:
        conn.close()

def add_record():
    """
    Add a new record to the 'members' table.
    """
    try:
        conn = sqlite3.connect("wanghong.db")
        cursor = conn.cursor()

        mname = input("請輸入姓名: ")
        msex = input("請輸入性別: ")
        mphone = input("請輸入手機: ")

        cursor.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)", (mname, msex, mphone))
        conn.commit()
        print("=>異動 1 筆記錄")

    except sqlite3.Error as e:
        print(f"Error adding record: {e}")
    finally:
        conn.close()

def modify_record():
    """
    Modify a record in the 'members' table.
    """
    try:
        conn = sqlite3.connect("wanghong.db")
        cursor = conn.cursor()

        target_name = input("請輸入想修改記錄的姓名: ")

        if not target_name:
            print("=>必須指定姓名才可修改記錄")
            return

        new_msex = input("請輸入要改變的性別: ")
        new_mphone = input("請輸入要改變的手機: ")

        cursor.execute("SELECT * FROM members WHERE mname=?", (target_name,))
        record = cursor.fetchone()

        if record is not None:
            print("\n原資料：")
            print(f"姓名：{record[1]}，性別：{record[2]}，手機：{record[3]}")

            cursor.execute("UPDATE members SET msex=?, mphone=? WHERE mname=?", (new_msex, new_mphone, target_name))
            conn.commit()
            print("=>異動 1 筆記錄")

            print("修改後資料：")
            print(f"姓名：{record[1]}，性別：{new_msex}，手機：{new_mphone}")
        else:
            print(f"=>找不到姓名為 {target_name} 的記錄")

    except sqlite3.Error as e:
        print(f"Error modifying record: {e}")
    finally:
        conn.close()

def query_by_phone():
    """
    Query records by phone number.
    """
    try:
        conn = sqlite3.connect("wanghong.db")
        cursor = conn.cursor()

        target_phone = input("請輸入想查詢記錄的手機: ")

        cursor.execute("SELECT * FROM members WHERE mphone=?", (target_phone,))
        records = cursor.fetchall()

        if not records:
            print("=>查無資料")
        else:
            print("\n姓名　　　　性別　手機\n" + "-" * 29)
            for record in records:
                print(f"{record[1]:<8}　{record[2]:<2}　{record[3]}")

    except sqlite3.Error as e:
        print(f"Error querying records: {e}")
    finally:
        conn.close()

def delete_all_records():
    """
    Delete all records from the 'members' table.
    """
    try:
        conn = sqlite3.connect("wanghong.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM members")
        conn.commit()
        print(f"=>異動 {conn.total_changes} 筆記錄")

    except sqlite3.Error as e:
        print(f"Error deleting records: {e}")
    finally:
        conn.close()
