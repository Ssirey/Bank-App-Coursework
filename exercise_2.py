# Задание 2 - Приложение для банка. 
#
# Студент: Тархов Павел Андреевич
# Дата: 02.06.2021

import PySimpleGUI as sg


# Класс владельца счета, хранящий информацию о идентефикаторе имени и количестве денег
class User(object):
    userIdCounter = 0
    def __init__(self, name, cash = 0):
        self.userIdCounter += 1
        self.id = User.getNewId()
        self.name = name
        self.cash = int(cash)

    # Генератор id
    @classmethod 
    def getNewId(cls):
        cls.userIdCounter += 1
        return cls.userIdCounter

    # Информация о пользователе в формате списка
    def inArr(self):
        return [self.id, self.name, self.cash]
    
    # Добавить деньги на счет
    def deposit(self, cash):
        self.cash += cash
    
    # Списать деньги с счета
    def withdraw(self, cash):
        self.cash -= cash
    
    # Увеличить сумму на процент
    def income(self, percent):
        if self.cash > 0:
            self.cash *= int(1 + percent/100)
    
    # Перевести деньги другому User
    def transfer(self, otherUser, cash):
        self.withdraw(cash)
        otherUser.deposit(cash)

    # Возвращает количество денег у User
    def balance(self):
        return self.cash


# Список пользователей. 
class UserList(object):
    def __init__(self):
        self._data = list()

    # возвращает пользователей в формате списка
    def getUsers(self):
        return self._data

    # проверяет находится ли пользователь в списке
    def hasUser(self, userName):
        for user in self._data:
            if userName == user.name:
                return True
        return False
    
    # возвращает пользователя
    def getUser(self, userName):
        for user in self._data:
            if userName == user.name:
                return user

    # возвращает пользователя, а в случае, если пользователь не был найден создает нового и возвращает его
    def getOrCreate(self, userName):
        for user in self._data:
            if userName == user.name:
                return user
        newUser = User(userName)
        self.add(newUser)
        return newUser
    
    # возвращает многомерный массив с данными пользователей
    def makeData(self):
        data = []
        for user in self._data:
            data.append(user.inArr())
        return data

    # добавляет пользователя
    def add(self, user):
        self._data.append(user)


# обработчик команд
# выполняет команду и возвращает лог о выполнении
class CmdHandler(object):
    def __init__(self, userList):
        self.usersList = userList

    def deposit(self, userName, cash):
        self.usersList.getOrCreate(userName).deposit(int(cash))
        return userName + "'s account balance has been increased by " + str(cash)

    def withdraw(self, userName, cash):
        self.usersList.getOrCreate(userName).withdraw(int(cash))
        return userName + "'s account balance has been decreased by " + str(cash)

    def balance(self, userName):
        user = self.usersList.getUser(userName)
        return "NO CLIENT" if user == None else userName + "'s account balance is " + str(user.balance())

    def transfer(self, userName1, userName2, cash):
        self.usersList.getOrCreate(userName1).transfer(self.usersList.getOrCreate(userName2) , int(cash))
        return cash + " was transferred from " + userName1 + "'s account to " + userName2 + "'s account"

    def income(self, percent):
        for user in self.usersList.getUsers():
            user.income(float(percent))
        return "Accrual of interest on accounts"

    # получает на вход текст парсит его на команды и запускает команды в работу.
    def parseTextToCmdAndRun(self, cmdText):
        message = ""
        cmdText = cmdText.strip().split()
        if len(list(filter(lambda el: el in self.commandDict.keys(), cmdText))) > 20:
            return "The maximum number of commands in the terminal is 20. Enter fewer commands."
        i = 0
        # print(cmdText)
        while i < len(cmdText):
            cmdKeys = self.commandDict.keys()
            if cmdText[i] in cmdKeys:
                func = self.commandDict[cmdText[i]][0]
                argsAmount = self.commandDict[cmdText[i]][1]
                result = func(self, *cmdText[i+1: i + argsAmount + 1])
                message += result + '\n'
                i += int(argsAmount)
            else:
                i += 1
        return message

    commandDict = {
        # имя команды : [функция : количество аргументов]
        "DEPOSIT"   : [deposit, 2],
        "WITHDRAW"  : [withdraw, 2],
        "BALANCE"   : [balance, 1],
        "TRANSFER"  : [transfer, 3],
        "INCOME"    : [income, 1]
    }

usersList = UserList()
usersList.add(User("Tarkhoff", 70153452))

commandHandler = CmdHandler(usersList)


layout = [
    [sg.Table(key="users", values = usersList.makeData(), headings=["ID", "Name", 'Cash'], auto_size_columns=False, col_widths=[11, 35, 35])],
    [sg.MLine(key="inputML", size=(50, 30)), sg.MLine(key="outputML"+sg.WRITE_ONLY_KEY, size=(50, 30), disabled=True)],
    [sg.Button("Calculate"), sg.Button("Clear")]
]

window = sg.Window('Bank app', layout)

while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == "Calculate":
        message = commandHandler.parseTextToCmdAndRun(values["inputML"])
        window["outputML"+sg.WRITE_ONLY_KEY].print(message)
        window["users"].update(usersList.makeData())
    if event == "Clear":
        window["outputML"+sg.WRITE_ONLY_KEY].update("")
        window["inputML"].update("")