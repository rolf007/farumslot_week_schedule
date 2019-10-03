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


layout = landscape(A4)
day_width = 53
day_height = 73
person_width = 118
person_height = 25
food_height = 78
food_width = 250


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER
styleBH.fontSize=14

styleNotes = ParagraphStyle("Notes")
styleNotes.alignment = TA_LEFT
styleNotes.fontSize=14

styleFoodField = ParagraphStyle("FoodField")
styleFoodField.alignment = TA_LEFT
styleFoodField.fontSize=14

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
img_Dannebrog = Image("Dannebrog.png", day_height/6, day_height/6)
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

def mk_simple_note(name):
    return RTalbe(Paragraph(name, style=styleNotes), None, None)

def mk_birthday_note(name):
    content = RTalbe(Paragraph(name, style=styleNotes), person_width, 15)
    frame_size = 30
    frame_color = col_K
    subtable = Table([[img_Dannebrog,content.table]], colWidths = [frame_size, content.w], rowHeights=[content.h])

    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('BACKGROUND',(0,0),(-1,-1),HexColor("#ffffff")),
                           ('LEFTPADDING',(0,0),(-1,-1), 0),
                           ('RIGHTPADDING',(0,0),(-1,-1), 0),
                           ('TOPPADDING',(0,0),(-1,-1), 0),
                           ('BOTTOMPADDING',(0,0),(-1,-1), 0)
                           ]))
    return RTalbe(subtable, content.w + frame_size, content.h)

    return mk_frame_lr(RTalbe(Paragraph(name, style=styleNotes), person_width-60, 15), 30, col_K)

def mk_week_day(name):
    return RTalbe(Paragraph(name, style=styleBH), None, None)

def mk_big_task(name, color):
    return mk_frame_lr(RTalbe(Paragraph(name, style=styleBH), person_width-10, 15), 5, color)

def mk_food_task(name, color):
    return mk_frame_lr(RTalbe(Paragraph(name, style=styleBH), person_width-60, 15), 30, color)

def mk_person(name, color):
    return mk_frame_tb(RTalbe(Paragraph(name, style=styleBH), person_width, 15), 5, color)

def mk_food_field(color, name, eaters):
    food_frame_width = 5
    inner_food = mk_inner_food(mk_frame(RTalbe(Paragraph(name, style=styleFoodField),food_width-food_height/3-2*food_frame_width,day_height-2*food_frame_width), 5, color).table, food_width, eaters)
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
        MarkDay(year=None, month=1, day=1, name="Nyt&aring;rsdag", type=MarkDayType.Note),
        MarkDay(year=None, month=1, day=6, name="Hellig tre konger", type=MarkDayType.Note),
        MarkDay(year=None, month=2, day=14, name="Valentinsdag", type=MarkDayType.Note),
        MarkDay(year=None, month=6, day=23, name="Sankt Hans Aften", type=MarkDayType.Note),
        MarkDay(year=None, month=6, day=5, name="Fars dag", type=MarkDayType.Note),
        MarkDay(year=None, month=6, day=5, name="Grundlovsdag", type=MarkDayType.Note),
        MarkDay(year=None, month=10, day=31, name="Halloween", type=MarkDayType.Note),
        MarkDay(year=None, month=11, day=10, name="Mortens Aften", type=MarkDayType.Note),
        MarkDay(year=None, month=12, day=24, name="Juleaftens dag", type=MarkDayType.Holiday),
        MarkDay(year=None, month=12, day=25, name="Juledag", type=MarkDayType.Holiday),
        MarkDay(year=None, month=12, day=26, name="2. Juledag", type=MarkDayType.Holiday),
        MarkDay(year=None, month=12, day=31, name="Nyt&aring;rsaften", type=MarkDayType.Holiday),


        MarkDay(month= 1, day= 7, name="Victor"       ,year=2013, type=MarkDayType.Birthday),
        MarkDay(month= 1, day=13, name="Cecilia"      ,year=2001, type=MarkDayType.Birthday),
        MarkDay(month= 1, day=19, name="Ellen"        ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 2, day= 9, name="Rolf"         ,year=1975, type=MarkDayType.Birthday),
        MarkDay(month= 3, day=12, name="Kristine"     ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 3, day=16, name="Anita"        ,year=1943, type=MarkDayType.Birthday),
        MarkDay(month= 3, day=17, name="Sophia"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 3, day=18, name="Thor"         ,year=1973, type=MarkDayType.Birthday),
        MarkDay(month= 4, day= 8, name="Adam"         ,year=2005, type=MarkDayType.Birthday),
        MarkDay(month= 4, day= 8, name="Sune"         ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 4, day= 9, name="Marcus"       ,year=1985, type=MarkDayType.Birthday),
        MarkDay(month= 4, day=26, name="Pauline"      ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 5, day= 4, name="Christian"    ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 5, day= 5, name="Linda"        ,year=1979, type=MarkDayType.Birthday),
        MarkDay(month= 5, day=13, name="Erik"         ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 5, day=14, name="Miguel"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 5, day=26, name="Oscar William",year=None, type=MarkDayType.Birthday),
        MarkDay(month= 6, day= 5, name="Vibeke"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 6, day=10, name="Jacco"        ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 6, day=14, name="Martin"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 7, day= 3, name="Takako"       ,year=1974, type=MarkDayType.Birthday),
        MarkDay(month= 7, day=11, name="Henriette"    ,year=1970, type=MarkDayType.Birthday),
        MarkDay(month= 7, day=15, name="Tobias"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 7, day=24, name="Marie-Louise" ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 7, day=24, name="Wilhelm"      ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 8, day= 7, name="August"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 8, day=13, name="Disa"         ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 8, day=16, name="Trold"        ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 8, day=26, name="Maria"        ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 8, day=31, name="Oliver"       ,year=2008, type=MarkDayType.Birthday),
        MarkDay(month= 9, day= 7, name="Karen"        ,year=1973, type=MarkDayType.Birthday),
        MarkDay(month= 9, day=13, name="Helena"       ,year=2002, type=MarkDayType.Birthday),
        MarkDay(month= 9, day=13, name="Silja"        ,year=None, type=MarkDayType.Birthday),
        MarkDay(month= 9, day=23, name="Esben"        ,year=None, type=MarkDayType.Birthday),
        MarkDay(month=10, day=25, name="Gert"         ,year=1944, type=MarkDayType.Birthday),
        MarkDay(month=10, day=26, name="Sune"         ,year=None, type=MarkDayType.Birthday),
        MarkDay(month=11, day= 6, name="Ane-Helene"   ,year=None, type=MarkDayType.Birthday),
        MarkDay(month=11, day=11, name="Thomas"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month=11, day=24, name="Jakob"        ,year=1981, type=MarkDayType.Birthday),
        MarkDay(month=11, day=24, name="Karina"       ,year=1981, type=MarkDayType.Birthday),
        MarkDay(month=12, day=17, name="Arthur"       ,year=None, type=MarkDayType.Birthday),
        MarkDay(month=12, day=18, name="Samuel"       ,year=2006, type=MarkDayType.Birthday),

        MarkDay(year=2018, month=2, day=11, name="Fastelavn", type=MarkDayType.Note),
        MarkDay(year=2018, month=3, day=25, name="Palmes&oslash;ndag", type=MarkDayType.Note),
        MarkDay(year=2018, month=3, day=25, name="Sommertid starter", type=MarkDayType.Note),
        MarkDay(year=2018, month=3, day=29, name="Sk&aelig;rtorsdag", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=3, day=30, name="Langfredag", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=4, day=1, name="P&aring;skedag", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=4, day=2, name="2. P&aring;skedag", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=4, day=27, name="Store Bededag", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=5, day=10, name="Kristi Himmelfart", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=5, day=13, name="Mors dag", type=MarkDayType.Note),
        MarkDay(year=2018, month=5, day=20, name="Pinsedag", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=5, day=21, name="2. Pinsedag", type=MarkDayType.Holiday),
        MarkDay(year=2018, month=10, day=28, name="Sommertid slutter", type=MarkDayType.Note),

        MarkDay(year=2019, month=3, day=3, name="Fastelavn", type=MarkDayType.Note),
        MarkDay(year=2019, month=3, day=31, name="Sommertid starter", type=MarkDayType.Note),
        MarkDay(year=2019, month=4, day=14, name="Palmes&oslash;ndag", type=MarkDayType.Note),
        MarkDay(year=2019, month=4, day=18, name="Sk&aelig;rtorsdag", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=4, day=19, name="Langfredag", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=4, day=21, name="P&aring;skedag", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=4, day=22, name="2. P&aring;skedag", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=5, day=12, name="Mors dag", type=MarkDayType.Note),
        MarkDay(year=2019, month=5, day=17, name="Store Bededag", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=5, day=30, name="Kristi Himmelfart", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=6, day=9, name="Pinsedag", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=6, day=10, name="2. Pinsedag", type=MarkDayType.Holiday),
        MarkDay(year=2019, month=10, day=27, name="Sommertid slutter", type=MarkDayType.Note),

        MarkDay(year=2020, month=2, day=23, name="Fastelavn", type=MarkDayType.Note),
        MarkDay(year=2020, month=3, day=29, name="Sommertid starter", type=MarkDayType.Note),
        MarkDay(year=2020, month=4, day=5, name="Palmes&oslash;ndag", type=MarkDayType.Note),
        MarkDay(year=2020, month=4, day=9, name="Sk&aelig;rtorsdag", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=4, day=10, name="Langfredag", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=4, day=12, name="P&aring;skedag", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=4, day=13, name="2. P&aring;skedag", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=5, day=8, name="Store Bededag", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=5, day=10, name="Mors dag", type=MarkDayType.Note),
        MarkDay(year=2020, month=5, day=21, name="Kristi Himmelfart", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=5, day=31, name="Pinsedag", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=6, day=1, name="2. Pinsedag", type=MarkDayType.Holiday),
        MarkDay(year=2020, month=10, day=25, name="Sommertid slutter", type=MarkDayType.Note),

 ]
#https://www.kalender-365.dk/helligdage/2017.html

def yww2date(year, week, week_day):
    return datetime.datetime.strptime('%d-W%d-%s' % (year, week, week_day), "%G-W%V-%u") #"%Y-W%W-%w"

def is_holiday(year, week, week_day):
    if week_day ==6 or week_day == 7:
        return True
    date = yww2date(year, week, week_day)
    for markday in mark_days:
        if markday.type == MarkDayType.Holiday and (markday.year == date.year or markday.year == None) and markday.month == date.month and markday.day == date.day:
            return True
    return False

def get_mark_days(year, week, week_day):
    notes = []
    date = yww2date(year, week, week_day)
    for markday in mark_days:
        if markday.month == date.month and markday.day == date.day:
            if (markday.type == MarkDayType.Note or markday.type == MarkDayType.Holiday) and (markday.year == date.year or markday.year == None):
                notes.append(markday)
            if markday.type == MarkDayType.Aniversary or markday.type == MarkDayType.Birthday:
                notes.append(markday)
    return notes

def day_str(year, week, week_day):
    date = yww2date(year, week, week_day)
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

def main_table_style(year, week):
    style = [
             ('BACKGROUND',(0,0),(0,-1),HexColor("#C0C0C0")),
             ('VALIGN',(0,0),(-1,-1),"TOP"),
             ('LEFTPADDING',(0,0),(-1,-1), 0),
             ('RIGHTPADDING',(0,0),(-1,-1), 0),
             ('TOPPADDING',(0,0),(-1,-1), 0),
             ('BOTTOMPADDING',(0,0),(-1,-1), 0),
             ('GRID',(0,0),(-1,-1),1,(0,0,0,)),
             #('BOX', (2,2), (3,3), 6, HexColor("#00FF00"))
             ('FONT', (0,4), (-1,4), 'Helvetica-Bold'),
             ('FONTSIZE', (0, 4), (-1, -1), 21),
             ('TEXTFONT', (0, 0), (-1, -1), 'Times-Bold'),
             ]
    for day in range(Day.Monday.value, Day.Sunday.value+1):
        m = day
        if is_holiday(year, week, day):
            style.append(('BACKGROUND', (0, m), (0, m), HexColor("#ffdddd")))
    return style

def page0(year, week):
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
    add_task(fields, Day.Monday, Person.Header, mk_week_day("Mandag %s" % day_str(year, week, 1)))
    add_task(fields, Day.Tuesday, Person.Header, mk_week_day("Tirsdag %s" % day_str(year, week, 2)))
    add_task(fields, Day.Wednesday, Person.Header, mk_week_day("Onsdag %s" % day_str(year, week, 3)))
    add_task(fields, Day.Thursday, Person.Header, mk_week_day("Torsdag %s" % day_str(year, week, 4)))
    add_task(fields, Day.Friday, Person.Header, mk_week_day("Fredag %s" % day_str(year, week, 5)))
    add_task(fields, Day.Saturday, Person.Header, mk_week_day("L&oslash;rdag %s" % day_str(year, week, 6)))
    add_task(fields, Day.Sunday, Person.Header, mk_week_day("S&oslash;ndag %s" % day_str(year, week, 7)))

    add_task(fields, Day.Monday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Tuesday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Wednesday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Thursday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Friday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Saturday, Person.Rolf, mk_simple_task("Vande planter"))
    add_task(fields, Day.Sunday, Person.Rolf, mk_simple_task("Vande planter"))

    add_task(fields, Day.Saturday, Person.Rolf, mk_big_task("St&oslash;vsuge", col_R))

    if even_week:
        add_task(fields, Day.Friday, Person.Rolf, mk_food_task("Mad", col_R))
        add_task(fields, Day.Saturday, Person.Karen, mk_food_task("Mad", col_K))

    add_task(fields, Day.Monday, Person.Samuel, mk_food_task("Mad", col_S))
    add_task(fields, Day.Tuesday, Person.Adam, mk_food_task("Mad", col_A))
    add_task(fields, Day.Wednesday, Person.Rolf, mk_food_task("Mad", col_R))
    add_task(fields, Day.Thursday, Person.Cecilia, mk_food_task("Mad", col_C))
    add_task(fields, Day.Sunday, Person.Helena, mk_food_task("Mad", col_H))


    add_task(fields, Day.Monday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Tuesday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Wednesday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Thursday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Friday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Saturday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Sunday, Person.Karen, mk_simple_task("Vasket&oslash;j"))
    add_task(fields, Day.Wednesday, Person.Karen, mk_big_task("Nemlig", col_K))

    add_task(fields, Day.Monday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Tuesday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Wednesday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Thursday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Friday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Saturday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Sunday, Person.Cecilia, mk_big_task("T&oslash;m opvask", col_C))
    add_task(fields, Day.Saturday, Person.Cecilia, mk_big_task("Toilet", col_C))

    add_task(fields, Day.Saturday, Person.Helena, mk_big_task("Badev&aelig;relse", col_H))

    add_task(fields, Day.Wednesday, Person.Adam, mk_big_task("St&oslash;vsuge", col_A))
    add_task(fields, Day.Monday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Tuesday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Wednesday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Thursday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Friday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Saturday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Sunday, Person.Adam, mk_big_task("Ordne k&oslash;kken", col_A))
    add_task(fields, Day.Thursday, Person.Adam, mk_simple_task("Fodbold 16:15-17:30"))
    if even_week:
        add_task(fields, Day.Saturday, Person.Adam, mk_simple_task("Fodbold 12:00-13:20"))

    add_task(fields, Day.Tuesday, Person.Samuel, mk_simple_task("Fodbold kl 17:45-19:00"))
    add_task(fields, Day.Thursday, Person.Samuel, mk_simple_task("Fodbold kl 16:30-17:45"))
    add_task(fields, Day.Friday, Person.Samuel, mk_simple_task("Fodbold kl 15:30-17:45"))
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
    b.setStyle(main_table_style(year, week))
    return b

def page1(year, week):
    odd_week = bool(week%2)
    even_week = not odd_week

    fields = [[[] for i in Page1] for i in Day]

    add_task(fields, Day.Header, Page1.Food, mk_person("Mad", col_W))
    add_task(fields, Day.Header, Page1.Notes, mk_person("Noter", col_W))

    add_task(fields, Day.Header, Page1.Header, mk_week_day("Uge %d" % week))
    add_task(fields, Day.Monday, Page1.Header, mk_week_day("Mandag %s" % day_str(year, week, 1)))
    add_task(fields, Day.Tuesday, Page1.Header, mk_week_day("Tirsdag %s" % day_str(year, week, 2)))
    add_task(fields, Day.Wednesday, Page1.Header, mk_week_day("Onsdag %s" % day_str(year, week, 3)))
    add_task(fields, Day.Thursday, Page1.Header, mk_week_day("Torsdag %s" % day_str(year, week, 4)))
    add_task(fields, Day.Friday, Page1.Header, mk_week_day("Fredag %s" % day_str(year, week, 5)))
    add_task(fields, Day.Saturday, Page1.Header, mk_week_day("L&oslash;rdag %s" % day_str(year, week, 6)))
    add_task(fields, Day.Sunday, Page1.Header, mk_week_day("S&oslash;ndag %s" % day_str(year, week, 7)))

    if odd_week:
        add_task(fields, Day.Friday, Page1.Food, mk_food_field(col_W, "", "RK"))
        add_task(fields, Day.Saturday, Page1.Food, mk_food_field(col_W, "", "RK"))

    if even_week:
        add_task(fields, Day.Friday, Page1.Food, mk_food_field(col_R, "Rolf:", "RKCHAS"))
        add_task(fields, Day.Saturday, Page1.Food, mk_food_field(col_K, "Karen:", "RKCHAS"))


    add_task(fields, Day.Monday, Page1.Food, mk_food_field(col_H, "Helena:", "RKCHAS"))
    add_task(fields, Day.Tuesday, Page1.Food, mk_food_field(col_A, "Adam:", "RKCHAS"))
    add_task(fields, Day.Wednesday, Page1.Food, mk_food_field(col_S, "Samuel:", "RKCHAS"))
    add_task(fields, Day.Thursday, Page1.Food, mk_food_field(col_C, "Cecilia:", "RKCHAS"))

    add_task(fields, Day.Sunday, Page1.Food, mk_food_field(col_R, "Rolf:", "RKCHAS"))

    for day in Day:
        if day == Day.Header:
            continue
        for note in get_mark_days(year, week, day.value):
            if note.type == MarkDayType.Birthday:
                add_task(fields, day, Page1.Notes, mk_birthday_note(note.name))
            else:
                add_task(fields, day, Page1.Notes, mk_simple_note(note.name))

    data = []
    for day in Day:
        row = []
        for person in Page1:
            row.append(make_field_table(fields[day.value][person.value]))
        data.append(row)

    b = Table(data, colWidths=[day_width,food_width,food_width],
            rowHeights=[person_height, day_height, day_height, day_height, day_height, day_height, day_height, day_height])
    b.hAlign = "LEFT"
    b.setStyle(main_table_style(year, week))
    return b


Story=[]
year = 2019
for week in range(40, 54):
    #Story.append(page0(year, week))
    #Story.append(PageBreak())
    Story.append(page1(year, week))
    Story.append(PageBreak())

doc = SimpleDocTemplate("form_letter.pdf",pagesize=layout, rightMargin=35,leftMargin=35, topMargin=15,bottomMargin=5)
doc.build(Story)
