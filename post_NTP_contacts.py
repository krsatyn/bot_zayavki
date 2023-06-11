from database_function import post_NTP_contscts

print("Добавление записис в Статус заявки, сделано для демонстрации")
full_name = str(input("Введите ФИО:\n"))
phone_number = str(input("Введите номер телефона:\n"))
email = str(input("Введите почту:\n"))
post_NTP_contscts(full_name=full_name, phone_number=phone_number, email=email)