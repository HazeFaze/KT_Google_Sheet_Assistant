import datetime
from modules.autocomplete_list import dealer_list, citizenship_list, document_type_list, employee_list
from modules.post_data import write_logg
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QCompleter, QApplication

app = QApplication([])
ui = uic.loadUi("ui/main.ui")

# Настройка автозаполнения и настройка
dealer_completer = QCompleter(dealer_list)
dealer_completer.setCaseSensitivity(2)
dealer_completer.setFilterMode(QtCore.Qt.MatchFlag(1))
citizenship_completer = QCompleter(citizenship_list)
citizenship_completer.setCaseSensitivity(2)
citizenship_completer.setFilterMode(QtCore.Qt.MatchFlag(1))
document_type_completer = QCompleter(document_type_list)
document_type_completer.setCaseSensitivity(2)
document_type_completer.setFilterMode(QtCore.Qt.MatchFlag(1))
employee_completer = QCompleter(employee_list)
employee_completer.setCaseSensitivity(2)
employee_completer.setFilterMode(QtCore.Qt.MatchFlag(1))
ui.phone_dealer.setCompleter(dealer_completer)
ui.citizenship.setCompleter(citizenship_completer)
ui.document_type.setCompleter(document_type_completer)
ui.employee.setCompleter(employee_completer)


def clear_fields():
    # Очистка полей ввода
    ui.client_name.clear()
    ui.client_name.clear()
    ui.phone_dealer.clear()
    ui.document_type.clear()
    ui.citizenship.clear()
    ui.price.clear()
    ui.client_phone.clear()
    ui.document_theme.clear()
    ui.adress.clear()
    ui.employee.clear()


def post_new_data(body):
    # Импорт и создание экземпляра класса
    from modules.post_data import Post_to_document
    result = Post_to_document(body)

    # Опопвещение пользователия и очистка полей
    if result:
        clear_fields()
        ui.output_message.setText(f'Добавлена новая запись: {body[0][0:7] + body[0][12:]}')
    else:
        ui.output_message.setText('Произошла ошибка, запись не добавлена!!!')


def button_push():
    # Привязка полей формы
    date_time = datetime.datetime.now().strftime("%d/%m/%y")
    client_name = ui.client_name.text()
    phone_dealer = ui.phone_dealer.text()
    document_type = ui.document_type.text()
    citizenship = ui.citizenship.text()
    order_price = ui.price.text()
    client_phone = ui.client_phone.text()
    document_theme = ui.document_theme.text()
    client_address = ui.adress.text()
    employee = ui.employee.text()

    body = [[client_name.upper(), phone_dealer.upper(), document_type.upper(),
             citizenship.upper(), order_price, client_phone, date_time, employee.upper(),
             None, None, None, None,
             document_theme.upper(), client_address.upper()]]

    # Проверка на ввод обязательных параметров
    if len(client_name) == 0:
        ui.output_message.setText('Поле "ФИО" не может быть пустым')
        write_logg(f'{datetime.datetime.now()} | Некорректный ввод данных: {body[0][0:7] + body[0][12:]}' + '\n')
    elif len(phone_dealer) == 0:
        ui.output_message.setText('Поле "Телефон/Дилер" не может быть пустым')
        write_logg(f'{datetime.datetime.now()} | Некорректный ввод данных: {body[0][0:7] + body[0][12:]}' + '\n')
    elif len(document_type) == 0:
        ui.output_message.setText('Поле "Услуга" не может быть пустым')
        write_logg(f'{datetime.datetime.now()} | Некорректный ввод данных: {body[0][0:7] + body[0][12:]}' + '\n')
    elif len(order_price) == 0:
        ui.output_message.setText('Поле "Цена" не может быть пустым')
        write_logg(f'{datetime.datetime.now()} | Некорректный ввод данных: {body[0][0:7] + body[0][12:]}' + '\n')
    else:
        write_logg(f'{datetime.datetime.now()} | Попытка добавить запись: {body[0][0:7] + body[0][12:]}' + '\n')
        post_new_data(body)


ui.push_button.clicked.connect(button_push)
ui.btn_clear.clicked.connect(clear_fields)


def main():
    ui.output_message.setText('Заполните поля помеченные *')
    ui.show()
    app.exec()


if __name__ == '__main__':
    main()
