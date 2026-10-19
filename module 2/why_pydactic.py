def insert_student(name,math,english):
    print("name :", name)
    if type(math)==int and type(english) == int:
        total = math + english
        print("total :", total)
        # print(type(math))
    else:
        print("wrong")

insert_student("Riaz",12,23)