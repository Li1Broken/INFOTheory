#импорт библиотек для работы
import math
from tkinter import *
from tkinter import ttk
import re
import sympy



#создание окна графического дизайна и его параметры
root = Tk()
#название окна
root.title("Calculator")
#размер окна
root.geometry("300x217")
#список кнопок для клавиратуры калькулятора
bttn_list = [
"1", "2", "3",
"4", "5", "6",
"7", "8", "9",
"(", "0", ")",
"+", "*", "-",
"/", "C", "=",
"(mod"
 ]

r = 3 #строка, с которой начнутся кнопки
c = 0 #колонка с кнопками, с которой начнется клавиатура

#цикл для создания кнопок
for i in bttn_list:
    rel = ""
    cmd=lambda x=i: calc(x)
    #параметры, которые будут присвоены всем кнопкам из списка
    ttk.Button(root, text=i, command = cmd, width = 15).grid(row=r, column = c)
    c += 1  #после создания одной из кнопок, мы переходим к следущей колонке из строки, пока не дойдем до третьей колонки
    if c > 2: #когда дошли до третьей колонки, мы переходим к нулевой колонке следущего ряда
        c = 0
        r += 1

#создание окошка, в которое будет вводится искомое выражение, и его параметры
calc_entry = Entry(root, width = 48)
calc_entry.grid(row=0, column=0, columnspan=5)
#чтобы кнопки и окошко ввода не слипались, создана "пустая строка"
lbl=Label(root, fg="#000000")
lbl.grid(row=2, column = 0, columnspan=5)

#функция, с помощью которой производятся все вычисления
def calc(key):

    global memory
    #условный оператор, который отзывается на нажатие некоторых клавишь
    if key == "=":
        findalf = str(calc_entry.get())
        findalf = findalf.replace('mod', '')
        regexp1 = r"([a-zA-Z])"
        match= re.search(regexp1, findalf)
        if match == None:
            # если нажали равно, то мы начинаем процесс вычисления
            string = str(calc_entry.get())
            # получаем выраение, которое надо вычислить
            # находим модуль, который вписан в выражение
            # для этого мы находим "d"
            mod01 = string.find("d")
            # метод .find() находит индекс, под которым находится нужный символ в строке
            # с помощью найденного индекса обрезаем строку так, чтобы условно из "1+1...(mod31)" получилось "31)"
            string = string[mod01 + 1:]
            # тем же методом .find() находим индекс ")" и обрезаем его. Таким образом, мы нашли значение модуля
            mod02 = string.find(")")
            mod03 = string[:mod02]
            mod = int(mod03)
            if sympy.ntheory.primetest.isprime(mod) == True:
                # в послую строку закладываем строчку со знаком деления
                fd = "/"
                global expression
                # создаем условный цикл, который проверяет, есть ли в выражении, которое надопосчитать, знак деления
                if fd in calc_entry.get():
                    # если есть, то начинается поиск обратного элемента
                    # в переменную закладываем изначальное выражение
                    result = str(calc_entry.get())
                    # ищем в нем, под каким индексом расположен знак деления, обрезаем выражение с "1+1/17(mod31)" до "17(mod31)"
                    index_del = result.find("/")
                    m = result[index_del + 1:]
                    # дальше круче. В ход вступают регулярные выражения
                    # в эту переменную с помощью регулярных выражени я заложила параметры поиска
                    regexp = r"(\d+)"
                    # (мне из полученной выше строки нужно вычленить все цифры, которые располагаются от начала новой строки до первого знака препинания)
                    # поиск осуществляется через метод re.
                    a = re.search(regexp, m)
                    kk = result.rfind(a[0])
                    a = int(a[0])  # тадаааааа, число, для которого надо найти обратное
                    # начинаем цикл для поиска обратного
                    # в цикле по формуле нахождения обратного цисла мы подставляем все i, j от 0 до 100
                    i = 0
                    j = 0
                    a_new = 0

                    for i in range(100):
                        for j in range(100):
                            # первое число i, которое подойдет в формуле, и будет обратным числом
                            if ((i * a) + (j * mod) == 1) or ((i * a) - (j * mod) == 1):
                                a_new = i
                                # теперь начинаем вычисление выражения
                                # опять берем изначалье выражение, заменияем в нем сначала '/' на '*', а потом число на обратное число
                                # обрезаем выражение
                                # терерь из выражения "1+1/17(mod31)" мы получили "1+1*11"
                                expression = result
                                expression = expression.replace('/', '*')
                                expression = expression.replace(str(a), str(a_new))
                                zz = expression.find("(")
                                expression = expression[:zz]
                                # с помощью метода eval() считаем выражение
                                total1 = eval(str(expression))
                                # находим остаток от деления, что является нахождением по модулю, и выводим в изначальную строку ввода
                                total = int(total1) % mod
                                total = " X=" + str(total)
                                calc_entry.insert(END, total)

                            else:
                                j += 1
                        i += 1
                        if a_new != 0:
                            break
                else:
                    # если деления нет, то по тому же принципу обрезаем скобки и то, что в них
                    result = str(calc_entry.get())
                    index_mod = result.find("(")
                    # считаем полученный результат
                    total1 = eval(result[:index_mod])
                    # если в выражении был минус и ответ стал отрицательным, то мы к ответы прибавляем модуль, который нашли ранее
                    if int(total1) < 0:
                        total1 = int(total1) + mod
                    # ищем ответ по модулю и выводим
                    total = int(total1) % mod
                    total = " X=" + str(total)
                    calc_entry.insert(END, total)
            else:
                calc_entry.insert(END, " Ошибка, число не простое")
        else:
            calc_entry.insert(END, " Ошибка, неправильное выражение")


    #если нажали на эту кнопку, по она стирает все, что записани в строку
    elif key == "C":
        calc_entry.delete(0, END)

    #добавление скобки
    elif key == "(":
        calc_entry.insert(END, "(")
    elif key == ")":
        calc_entry.insert(END, ")")

    else:
        if "=" in calc_entry.get():
            calc_entry.delete(0, END)
        calc_entry.insert(END, key)
root.mainloop()