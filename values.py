def depts():
    return [
        ("Dentistry","Dentistry"),
        ("Cardiology","Cardiology"),
        ("ENT","ENT"),
        ("Neurology","Neurology"),
        ("Blood","Blood Screening"),
        ("Virology","Virology")
    ]

def locs():
    return [
        ("1","Location 1"),
        ("2","Location 2"),
        ("3","Location 3"),
        ("4","Location 4")
    ]

def days():
    days = []
    for i in range(1,32):
        days.append((str(i),str(i)))
    return days

def month():
    return [
        ("1","January"),
        ("2","February"),
        ("3","March"),
        ("4","April"),
        ("5","May"),
        ("6","June"),
        ("7","July"),
        ("8","August"),
        ("9","September"),
        ("10","October"),
        ("11","November"),
        ("12","December")
    ]

def year():
    return [
        ("2020","2020"),
        ("2021","2021"),
        ("2022","2022")
    ]
    