from lib import read_credentials, create_database_and_table, import_data_from_file, display_menu, show_all_records, add_record, modify_record, query_by_phone, delete_all_records

def main():
    credentials = read_credentials("pass.json")

    username = input("請輸入帳號：")
    password = input("請輸入密碼：")

    if {"帳號": username, "密碼": password} not in credentials:
        print("=>帳密錯誤，程式結束")
        return

    while True:
        display_menu()
        choice = input("請輸入您的選擇 [0-7]: ")

        if choice == "0":
            break
        elif choice == "1":
            create_database_and_table()
        elif choice == "2":
            import_data_from_file("members.txt")
        elif choice == "3":
            show_all_records()
        elif choice == "4":
            add_record()
        elif choice == "5":
            modify_record()
        elif choice == "6":
            query_by_phone()
        elif choice == "7":
            delete_all_records()
        else:
            print("=>無效的選擇")

if __name__ == "__main__":
    main()
