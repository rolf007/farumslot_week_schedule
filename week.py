#!/bin/env python3

import reportlab
import datetime

from enum import Enum
from reportlab.lib.pagesizes import A4, landscape, portrait

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import PageTemplate, BaseDocTemplate, NextPageTemplate, PageBreak

col_K = HexColor("#ff150f")
col_A = HexColor("#000080")
col_R = HexColor("#75ff31")
col_C = HexColor("#ffff07")
col_S = HexColor("#1da7ff")
col_H = HexColor("#6f0511")
col_W = HexColor("#ffffff")

year = 2017
week = 47

if False:
    layout = portrait(A4)
    day_width = 45
    day_height = 109
    person_width = 76
    person_height = 25
    food_height = 70
else:
    layout = landscape(A4)
    day_width = 45
    day_height = 78
    person_width = 123
    person_height = 25
    food_height = 78
    food_width = 250


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

styleBH = styles["Normal"]
styleBH.alignment = TA_LEFT

class RTalbe:
    def __init__(self, table, w, h):
        self.table = table
        self.w = w
        self.h = h

class Person(Enum):
    Header = 0
    Rolf = 1
    Karen = 2
    Cecilia = 3
    Helena = 4
    Adam = 5
    Samuel = 6

class Page1(Enum):
    Header = 0
    Food = 1
    Notes = 2

class Day(Enum):
    Header = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

img_R = Image("R.png", day_height/6, day_height/6)
img_K = Image("K.png", day_height/6, day_height/6)
img_C = Image("C.png", day_height/6, day_height/6)
img_H = Image("H.png", day_height/6, day_height/6)
img_A = Image("A.png", day_height/6, day_height/6)
img_S = Image("S.png", day_height/6, day_height/6)
def mk_inner_food(fun, width, eaters):
    square = food_height/6
    subtable = Table([
        [fun,  img_R if 'R' in eaters else ' ',""],
        ["",   img_K if 'K' in eaters else ' ',""],
        ["",   img_C if 'C' in eaters else ' ',""],
        ["",   img_H if 'H' in eaters else ' ',""],
        ["",   img_A if 'A' in eaters else ' ',""],
        ["",   img_S if 'S' in eaters else ' ',""]
        ], colWidths = [width-2*square, square, square], rowHeights=[square, square, square, square, square, square])
    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('BACKGROUND',(1,0),(1,0),col_R),
                           ('BACKGROUND',(1,1),(1,1),col_K),
                           ('BACKGROUND',(1,2),(1,2),col_C),
                           ('BACKGROUND',(1,3),(1,3),col_H),
                           ('BACKGROUND',(1,4),(1,4),col_A),
                           ('BACKGROUND',(1,5),(1,5),col_S),
                           ('GRID',(1,0),(-1,-1),1,(0,0,0,)),
                           ('SPAN',(0,0),(0,5)),
                           ('LEFTPADDING',(0,0),(-1,-1), 0),
                           ('RIGHTPADDING',(0,0),(-1,-1), 0),
                           ('TOPPADDING',(0,0),(-1,-1), 0),
                           ('BOTTOMPADDING',(0,0),(-1,-1), 0)
                           ]))
    return RTalbe(subtable, width, food_height)

def mk_frame(content, frame_size, frame_color):
    subtable = Table([["","",""],["",content.table,""],["","",""]], colWidths = [frame_size, content.w, frame_size], rowHeights=[frame_size, content.h, frame_size])

    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('BACKGROUND',(0,0),(-1,-1),frame_color),
                           ('BACKGROUND',(1,1),(1,1),HexColor("#ffffff")),
                           ('LEFTPADDING',(1,1),(1,1), 0),
                           ('RIGHTPADDING',(1,1),(1,1), 0),
                           ('TOPPADDING',(1,1),(1,1), 0),
                           ('BOTTOMPADDING',(1,1),(1,1), 0)
                           ]))
    return RTalbe(subtable, content.w + 2*frame_size, content.h + 2*frame_size)

def mk_frame_lr(content, frame_size, frame_color):
    subtable = Table([["",content.table,""]], colWidths = [frame_size, content.w, frame_size], rowHeights=[content.h])

    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('BACKGROUND',(0,0),(-1,-1),frame_color),
                           ('BACKGROUND',(1,0),(1,0),HexColor("#ffffff")),
                           ('LEFTPADDING',(1,0),(1,0), 0),
                           ('RIGHTPADDING',(1,0),(1,0), 0),
                           ('TOPPADDING',(1,0),(1,0), 0),
                           ('BOTTOMPADDING',(1,0),(1,0), 0)
                           ]))
    return RTalbe(subtable, content.w + 2*frame_size, content.h)

def mk_frame_tb(content, frame_size, frame_color):
    subtable = Table([[""],[content.table],[""]], colWidths = [content.w], rowHeights=[frame_size, content.h, frame_size])

    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('BACKGROUND',(0,0),(-1,-1),frame_color),
                           ('BACKGROUND',(0,1),(0,1),HexColor("#ffffff")),
                           ('LEFTPADDING',(0,1),(0,1), 0),
                           ('RIGHTPADDING',(0,1),(0,1), 0),
                           ('TOPPADDING',(0,1),(0,1), 0),
                           ('BOTTOMPADDING',(0,1),(0,1), 0)
                           ]))
    return RTalbe(subtable, content.w, content.h + 2*frame_size)

def add_task(fields, day, person, task):
    fields[day.value][person.value].append(task)

def mk_simple_task(name):
    return RTalbe(Paragraph(name, style=styleBH), None, None)

def mk_week_day(name):
    return RTalbe(Paragraph(name, style=styleBH), None, None)

def mk_big_task(name, color):
    return mk_frame_lr(RTalbe(Paragraph(name, style=styleBH), person_width-10, 15), 5, color)

def mk_person(name, color):
    return mk_frame_tb(RTalbe(Paragraph(name, style=styleBH), person_width, 15), 5, color)

def mk_food_task(color, name, eaters):
    food_frame_width = 5
    inner_food = mk_inner_food(mk_frame(RTalbe(name,food_width-food_height/3-2*food_frame_width,day_height-2*food_frame_width), 5, color).table, food_width, eaters)
    return inner_food

class MarkDayType(Enum):
    Note = 0
    Aniversary = 1
    Birthday = 2
    Holiday = 3

class MarkDay:
    def __init__(self, year, month, day, name, type):
        self.year = year
        self.month = month
        self.day = day
        self.name = name
        self.type = type

mark_days = [
        MarkDay(year=2017, month=11, day=11, name="Mortens Aften", type=MarkDayType.Note),
        MarkDay(year=None, month=12, day=24, name="Juleaftens dag", type=MarkDayType.Holiday),
        MarkDay(year=2006, month=12, day=18, name="Samuel", type=MarkDayType.Birthday),
        MarkDay(year=2017, month=12, day=25, name="Juledag", type=MarkDayType.Holiday),
        MarkDay(year=2017, month=12, day=26, name="2. Juledag", type=MarkDayType.Holiday),
        MarkDay(year=2017, month=12, day=31, name="Nyt&aring;rsaften", type=MarkDayType.Holiday)
        ]
#https://www.kalender-365.dk/helligdage/2017.html

def is_holiday(year, week, week_day):
    if week_day ==6 or week_day == 7:
        return True
    date = datetime.datetime.strptime('%d-W%d-%s' % (year, week, week_day%7), "%Y-W%W-%w")
    for markday in mark_days:
        if markday.type == MarkDayType.Holiday and (markday.year == date.year or markday.year == None) and markday.month == date.month and markday.day == date.day:
            return True
    return False

def get_mark_days(year, week, week_day):
    notes = []
    date = datetime.datetime.strptime('%d-W%d-%s' % (year, week, week_day%7), "%Y-W%W-%w")
    for markday in mark_days:
        if markday.month == date.month and markday.day == date.day:
            if (markday.type == MarkDayType.Note or markday.type == MarkDayType.Holiday) and (markday.year == date.year or markday.year == None):
                notes.append(markday)
            if markday.type == MarkDayType.Aniversary or markday.type == MarkDayType.Birthday:
                notes.append(markday)
    return notes

def day_str(week_day):
    date = datetime.datetime.strptime('%d-W%d-%s' % (year, week, week_day%7), "%Y-W%W-%w")
    return date.strftime("%d %b")


def make_field_table(field):
    if field == []:
        return ""
    datax = []
    for i in field:
        datax.append([i.table])
    subtable = Table(datax)

    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('LEFTPADDING',(0,0),(-1,-1), 0),
                           ('RIGHTPADDING',(0,0),(-1,-1), 0),
                           ('TOPPADDING',(0,0),(-1,-1), 0),
                           ('BOTTOMPADDING',(0,0),(-1,-1), 0)
                           ]))
    return subtable

def main_table_style():
    style = [
             ('BACKGROUND',(0,0),(0,-1),HexColor("#C0C0C0")),
             ('VALIGN',(0,0),(-1,-1),"TOP"),
             ('LEFTPADDING',(0,0),(-1,-1), 0),
             ('RIGHTPADDING',(0,0),(-1,-1), 0),
             ('TOPPADDING',(0,0),(-1,-1), 0),
             ('BOTTOMPADDING',(0,0),(-1,-1), 0),
             ('GRID',(0,0),(-1,-1),1,(0,0,0,)),
             #('BOX', (2,2), (3,3), 6, HexColor("#00FF00"))
             ('FONT', (0,0), (0,0), 'Helvetica-Bold')
             ]
    for day in range(Day.Monday.value, Day.Sunday.value+1):
        m = day
        if is_holiday(year, week, day):
            style.append(('BACKGROUND', (0, m), (-1, m), HexColor("#ffdddd")))
    return style

def page0():
    odd_week = bool(week%2)
    even_week = not odd_week

    fields = [[[] for i in Person] for i in Day]

    add_task(fields, Day.Header, Person.Rolf, mk_person("Rolf", col_R))
    add_task(fields, Day.Header, Person.Karen, mk_person("Karen", col_K))
    add_task(fields, Day.Header, Person.Cecilia, mk_person("Cecilia", col_C))
    add_task(fields, Day.Header, Person.Helena, mk_person("Helena", col_H))
    add_task(fields, Day.Header, Person.Adam, mk_person("Adam", col_A))
    add_task(fields, Day.Header, Person.Samuel, mk_person("Samuel", col_S))

    add_task(fields, Day.Header, Person.Header, mk_week_day("Uge %d" % week))
    add_task(fields, Day.Monday, Person.Header, mk_week_day("Mandag %s" % day_str(1)))
    add_task(fields, Day.Tuesday, Person.Header, mk_week_day("Tirsdag %s" % day_str(2)))
    add_task(fields, Day.Wednesday, Person.Header, mk_week_day("Onsdag %s" % day_str(3)))
    add_task(fields, Day.Thursday, Person.Header, mk_week_day("Torsdag %s" % day_str(4)))
    add_task(fields, Day.Friday, Person.Header, mk_week_day("Fredag %s" % day_str(5)))
    add_task(fields, Day.Saturday, Person.Header, mk_week_day("L&oslash;rdag %s" % day_str(6)))
    add_task(fields, Day.Sunday, Person.Header, mk_week_day("S&oslash;ndag %s" % day_str(7)))

    #if even_week:
    #    add_task(fields, Day.Wednesday, Person.Header, mk_food_task(col_W, "RK"))
    #if odd_week:
    #    add_task(fields, Day.Friday, Person.Header, mk_food_task(col_W, "RK"))
    #    add_task(fields, Day.Saturday, Person.Header, mk_food_task(col_W, "RK"))

    add_task(fields, Day.Monday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Tuesday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Wednesday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Thursday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Friday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Saturday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Sunday, Person.Rolf, mk_simple_task("Vande planter"))
    if odd_week:
        add_task(fields, Day.Wednesday, Person.Rolf, mk_big_task("Mad", col_R))
        add_task(fields, Day.Sunday, Person.Rolf, mk_big_task("Mad", col_R))
    if even_week:
        add_task(fields, Day.Friday, Person.Rolf, mk_big_task("Mad", col_R))
    add_task(fields, Day.Saturday, Person.Rolf, mk_big_task("St&oslash;vsuge", col_R))


    add_task(fields, Day.Monday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Tuesday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Wednesday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Thursday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Friday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Saturday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Sunday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Wednesday, Person.Karen, mk_big_task("Nemlig", col_K))
    if even_week:
        add_task(fields, Day.Saturday, Person.Karen, mk_big_task("Mad", col_K))

    add_task(fields, Day.Monday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Tuesday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Wednesday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Thursday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Friday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Saturday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Sunday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Thursday, Person.Cecilia, mk_big_task("Mad", col_C))
    add_task(fields, Day.Saturday, Person.Cecilia, mk_big_task("Toilet", col_C))

    if even_week:
        add_task(fields, Day.Sunday, Person.Helena, mk_big_task("Mad", col_H))
    add_task(fields, Day.Saturday, Person.Helena, mk_big_task("Badev&aelig;relse", col_H))

    add_task(fields, Day.Tuesday, Person.Adam, mk_big_task("Mad", col_A))
    add_task(fields, Day.Wednesday, Person.Adam, mk_big_task("St&oslash;vsuge", col_A))
    add_task(fields, Day.Monday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Tuesday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Wednesday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Thursday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Friday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Saturday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Sunday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Thursday, Person.Adam, mk_simple_task("Fodbold"))
    if even_week:
        add_task(fields, Day.Saturday, Person.Adam, mk_simple_task("Fodbold"))

    add_task(fields, Day.Monday, Person.Samuel, mk_big_task("Mad", col_S))
    add_task(fields, Day.Tuesday, Person.Samuel, mk_simple_task("Fodbold kl 16:30"))
    add_task(fields, Day.Thursday, Person.Samuel, mk_simple_task("Fodbold kl 16:30"))
    add_task(fields, Day.Friday, Person.Samuel, mk_simple_task("Fodbold kl 15:00"))
    add_task(fields, Day.Monday, Person.Samuel, mk_big_task("Feje k&oslash;kken", col_S))
    add_task(fields, Day.Tuesday, Person.Samuel, mk_big_task("Feje k&oslash;kken", col_S))
    add_task(fields, Day.Wednesday, Person.Samuel, mk_big_task("Feje k&oslash;kken", col_S))
    add_task(fields, Day.Thursday, Person.Samuel, mk_big_task("Feje k&oslash;kken", col_S))
    add_task(fields, Day.Friday, Person.Samuel, mk_big_task("Feje k&oslash;kken", col_S))
    add_task(fields, Day.Saturday, Person.Samuel, mk_big_task("Feje k&oslash;kken", col_S))
    add_task(fields, Day.Sunday, Person.Samuel, mk_big_task("Feje k&oslash;kken", col_S))
    add_task(fields, Day.Monday, Person.Samuel, mk_big_task("D&aelig;k bord", col_S))
    add_task(fields, Day.Wednesday, Person.Samuel, mk_big_task("D&aelig;k bord", col_S))
    add_task(fields, Day.Saturday, Person.Samuel, mk_big_task("D&aelig;k bord", col_S))
    add_task(fields, Day.Sunday, Person.Samuel, mk_big_task("D&aelig;k bord", col_S))
    data = []
    for day in Day:
        row = []
        for person in Person:
            row.append(make_field_table(fields[day.value][person.value]))
        data.append(row)

    b = Table(data, colWidths=[day_width,person_width,person_width,person_width,person_width,person_width,person_width],
            rowHeights=[person_height, day_height, day_height, day_height, day_height, day_height, day_height, day_height])
    b.hAlign = "LEFT"
    b.setStyle(main_table_style())
    return b

def page1():
    odd_week = bool(week%2)
    even_week = not odd_week

    fields = [[[] for i in Page1] for i in Day]

    add_task(fields, Day.Header, Page1.Food, mk_person("Mad", col_W))
    add_task(fields, Day.Header, Page1.Notes, mk_person("Noter", col_W))

    add_task(fields, Day.Header, Page1.Header, mk_week_day("Uge %d" % week))
    add_task(fields, Day.Monday, Page1.Header, mk_week_day("Mandag %s" % day_str(1)))
    add_task(fields, Day.Tuesday, Page1.Header, mk_week_day("Tirsdag %s" % day_str(2)))
    add_task(fields, Day.Wednesday, Page1.Header, mk_week_day("Onsdag %s" % day_str(3)))
    add_task(fields, Day.Thursday, Page1.Header, mk_week_day("Torsdag %s" % day_str(4)))
    add_task(fields, Day.Friday, Page1.Header, mk_week_day("Fredag %s" % day_str(5)))
    add_task(fields, Day.Saturday, Page1.Header, mk_week_day("L&oslash;rdag %s" % day_str(6)))
    add_task(fields, Day.Sunday, Page1.Header, mk_week_day("S&oslash;ndag %s" % day_str(7)))

    if even_week:
        add_task(fields, Day.Wednesday, Page1.Food, mk_food_task(col_W, "", "RK"))
    if odd_week:
        add_task(fields, Day.Friday, Page1.Food, mk_food_task(col_W, "", "RK"))
        add_task(fields, Day.Saturday, Page1.Food, mk_food_task(col_W, "", "RK"))

    if odd_week:
        add_task(fields, Day.Wednesday, Page1.Food, mk_food_task(col_R, "Rolf:", "RKCHAS"))
        add_task(fields, Day.Sunday, Page1.Food, mk_food_task(col_R, "Rolf:", "RKCHAS"))
    if even_week:
        add_task(fields, Day.Friday, Page1.Food, mk_food_task(col_R, "Rolf:", "RKCHAS"))

    if even_week:
        add_task(fields, Day.Saturday, Page1.Food, mk_food_task(col_K, "Karen:", "RKCHAS"))

    add_task(fields, Day.Thursday, Page1.Food, mk_food_task(col_C, "Cecilia:", "RKCHAS"))
    if even_week:
        add_task(fields, Day.Sunday, Page1.Food, mk_food_task(col_H, "Helena:", "RKCHAS"))
    add_task(fields, Day.Tuesday, Page1.Food, mk_food_task(col_A, "Adam:", "RKCHAS"))
    add_task(fields, Day.Monday, Page1.Food, mk_food_task(col_S, "Samuel:", "RKCHAS"))

    for day in Day:
        if day == Day.Header:
            continue
        for note in get_mark_days(year, week, day.value):
            add_task(fields, day, Page1.Notes, mk_simple_task(note.name))

    data = []
    for day in Day:
        row = []
        for person in Page1:
            row.append(make_field_table(fields[day.value][person.value]))
        data.append(row)

    b = Table(data, colWidths=[day_width,food_width,food_width],
            rowHeights=[person_height, day_height, day_height, day_height, day_height, day_height, day_height, day_height])
    b.hAlign = "LEFT"
    b.setStyle(main_table_style())
    return b


Story=[]
Story.append(page0())
Story.append(PageBreak())
Story.append(page1())

doc = SimpleDocTemplate("form_letter.pdf",pagesize=layout, rightMargin=5,leftMargin=5, topMargin=5,bottomMargin=5)
doc.build(Story)
