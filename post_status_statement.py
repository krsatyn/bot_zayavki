from database_function import post_statement

#добавление элемента в бд
print("Добавление записис в Статус заявки, сделано для демонстрации")
number_statement = str(input("Введите номер заявки: "))
status_statement = str(input("Введите статус заявки "))
post_statement(number_statement, status_statement)