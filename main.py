import json
from tkinter import *
from operator import itemgetter
import tkinter.scrolledtext as st


# запись вектора публикации
def write_vector(vector, data_pub, classes, keyw, m):
    j = 1
    for value in classes.values():
        if value in data_pub[keyw]:
            vector.append(j + m)
        j += 1


# распаковка вектора (представление с помощью 0 и 1)
def unpack_vec(vect, k):
    un_vect = []
    for n in range(1, k):
        if n in vect:
            un_vect.append(1)
        else:
            un_vect.append(0)
    return un_vect


# определение метрики
def cosine_metric(vec1, vec2, k):
    a, b, c = 0, 0, 0
    u_vec1, u_vec2 = unpack_vec(vec1, k), unpack_vec(vec2, k)
    for n in range(0, k - 1):
        a += u_vec1[n]
        b += u_vec2[n]
        c += u_vec1[n]*u_vec2[n]
    a = a ** 0.5
    b = b ** 0.5
    if a * b != 0: return c/(a * b)
    else: return 0


# вычисление расстояний и ближайших публ.
def get_dist(pub_list, us, dis_list, near_pub, k):
    for publ in pub_list:
        di = cosine_metric(us, publ, k)
        dis_list.append(di)
        if di > 0:
            indi = indices(pub_list, publ)
            for j in indi:
                near_pub.append(j)


# составление словаря публ-расстояние
def get_dist_dict(distances, near_pub):
    publ_dict = {}
    for publ in near_pub:
        publ_dict[publ] = distances[publ]
    sorted_dict = dict(sorted(publ_dict.items(), key=itemgetter(1), reverse=True))
    return sorted_dict


def indices(lst, item):
    return [k for k, x in enumerate(lst) if x == item]


def get_selected_rub():
    lst = []
    lst.append(selected1.get())
    lst.append(selected2.get())
    lst.append(selected3.get())
    lst.append(selected4.get())
    lst.append(selected5.get())
    lst.append(selected6.get())
    lst.append(selected7.get())
    lst.append(selected8.get())
    return lst


def format_rec(pub_lst):
    rec = ""
    for publ in pub_lst.keys():
        p = data[publ]["text"]
        t = "Название: " + p["Название"] + "\n"
        t += "Рубрика: " + ", ".join(p["Рубрики"]) + "\n"
        t += "Язык: " + p["Язык"] + "\n"
        t += "Год: " + str(p["Год"]) + "\n"
        t += "URL: " + p["URL"] + "\n"
        rec += t + "\n"
    return rec


def set_recommendation(res, pubs):
    res.delete('6.0', END)
    res.insert(INSERT, format_rec(pubs))


# действие нажатия кнопки
def find_clicked():
    user = []
    selected_rub = get_selected_rub()
    for rub in selected_rub:
        if rub != 0:
            user.append(rub)
    if not user:
        result = Label(window, text="Пожалуйста, выберите хотя бы одну рубрику")
        result.place(x=0, y=200)
    else:
        nearest_pub = []
        distance_list = []
        keyword_amount = 98
        rub_amount = 8
        get_dist(publication_list_vectors_rub, user, distance_list, nearest_pub, rub_amount + keyword_amount)
        result = st.ScrolledText(window)
        result.place(x=0, y=200)
        dist_dict = get_dist_dict(distance_list, nearest_pub)
        set_recommendation(result, dist_dict)


# извлечение информации из json-файла
with open(r"C:\Users\user\PycharmProjects\content_filtering\data_pub", 'r', encoding="utf8") as publications_file:
    publications_data = json.load(publications_file)


# составление матрицы характеристик публикаций, где строка - вектор i-й публикации
data = publications_data['publication_list']
data_classes = publications_data['classes']
data_keywords = publications_data['key_words']
publication_list_vectors_rub = []
publication_list_vectors_keywords = []
i = 0
for pub in data:
    publication_list_vectors_rub.append([])
    publication_list_vectors_keywords.append([])
    write_vector(publication_list_vectors_rub[i], data[data.index(pub)]["text"], data_classes, "Рубрики", 0)
    write_vector(publication_list_vectors_keywords[i], data[data.index(pub)]["text"], data_keywords, "Ключевые слова", 8)
    for l in publication_list_vectors_keywords[i]:
        publication_list_vectors_rub[i].append(l)
    i += 1

# создание интерфейса
window = Tk()
window.title("Рекомендательная система")
window.geometry("700x600")
text_greet = Label(window, text="Выберите интересующие Вас рубрики:")
text_greet.place(x=0, y=0)

selected1 = IntVar()
rub1 = Radiobutton(window, text="Биология", value=1, variable=selected1)
rub1.place(x=20, y=40)

selected2 = IntVar()
rub2 = Radiobutton(window, text="Информатика", value=2, variable=selected2)
rub2.place(x=20, y=60)

selected3 = IntVar()
rub3 = Radiobutton(window, text="История", value=3, variable=selected3)
rub3.place(x=20, y=80)

selected4 = IntVar()
rub4 = Radiobutton(window, text="Математика", value=4, variable=selected4)
rub4.place(x=20, y=100)

selected5 = IntVar()
rub5 = Radiobutton(window, text="Медицина", value=5, variable=selected5)
rub5.place(x=300, y=40)

selected6 = IntVar()
rub6 = Radiobutton(window, text="Социология", value=6, variable=selected6)
rub6.place(x=300, y=60)

selected7 = IntVar()
rub7 = Radiobutton(window, text="Химия", value=7, variable=selected7)
rub7.place(x=300, y=80)

selected8 = IntVar()
rub8 = Radiobutton(window, text="Экономика", value=8, variable=selected8)
rub8.place(x=300, y=100)

btn_find = Button(window, text="Найти", command=find_clicked)
btn_find.place(x=20, y=140)

window.mainloop()
