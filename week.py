#!/bin/env python3

import reportlab

print("hello world")

from enum import Enum
from reportlab.lib.pagesizes import A4, landscape, portrait

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

doc = SimpleDocTemplate("form_letter.pdf",pagesize=portrait(A4),
                        rightMargin=0,leftMargin=0,
                        topMargin=0,bottomMargin=0)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

Story=[]

styleBH = styles["Normal"]
styleBH.alignment = TA_LEFT
#styleBH.borderWidth = 3
#styleBH.borderPadding = 1
#styleBH.borderColor = HexColor("#ff0000")
#styleBH.borderRadius = 0
#styleBH.spaceBefore=0
#styleBH.spaceAfter=0


day_width = 50
day_height = 109
human_width = 88
def make_inner_food(width, height, eaters):
    square = height/6
    subtable = Table([
        ["mad",'R' if 'R' in eaters else ' ',""],
        ["",   "K" if 'K' in eaters else ' ',""],
        ["",   "C" if 'C' in eaters else ' ',""],
        ["",   "H" if 'H' in eaters else ' ',""],
        ["",   "A" if 'A' in eaters else ' ',""],
        ["",   "S" if 'S' in eaters else ' ',""]
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
                           ('LEFTPADDING',(1,0),(-1,-1), 2),
                           ('RIGHTPADDING',(1,0),(-1,-1), 0),
                           ('TOPPADDING',(1,0),(-1,-1), 0),
                           ('BOTTOMPADDING',(1,0),(-1,-1), 0),
                           ('SPAN',(0,0),(0,5))
                           ]))
    return subtable

def mk_food_task(color, eaters):
    food_frame_width = 5
    food_height = 30
    subtable = Table([["","",""],["",make_inner_food(human_width-2*food_frame_width, day_height-2*food_frame_width-food_height, eaters),""],["","",""]], colWidths = [food_frame_width, human_width-2*food_frame_width, food_frame_width], rowHeights=[food_frame_width, day_height-2*food_frame_width-food_height, food_frame_width])

    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('BACKGROUND',(0,0),(-1,-1),color),
                           ('BACKGROUND',(1,1),(1,1),HexColor("#ffffff")),
                           ('LEFTPADDING',(1,1),(1,1), 0),
                           ('RIGHTPADDING',(1,1),(1,1), 0),
                           ('TOPPADDING',(1,1),(1,1), 0),
                           ('BOTTOMPADDING',(1,1),(1,1), 0)
                           ]))
    return (subtable, day_height-2*food_frame_width-food_height)

col_K = HexColor("#ff150f")
col_A = HexColor("#000080")
col_R = HexColor("#75ff31")
col_C = HexColor("#ffff07")
col_S = HexColor("#1da7ff")
col_H = HexColor("#6f0511")

data = [
        ["Uge 45", "Rolf", "Karen", "Cecilia", "Helena", "Adam", "Samuel"],
        ["Mandag", "", "", "", "", "", ""],
        ["Tirsdag", "", "", "", "", "", ""],
        ["Onsdag", "", "", "", "", "", ""],
        ["Torsdag", "", "", "", "", "", ""],
        ["Fredag", "", "", "", "", "", ""],
        [Paragraph("L&oslash;rdag", style=styleBH), "", "", "", "", "", ""],
        [Paragraph("S&oslash;ndag", style=styleBH), "", "", "", "", "", ""]]

fields = [[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]]]

def add_task(data, day, person, task):
    fields[day.value][person.value].append(task)


class Person(Enum):
    Rolf = 0
    Karen = 1
    Cecilia = 2
    Helena = 3
    Adam = 4
    Samuel = 5

class Day(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

def mk_simple_task(name):
    return (name, None)
week = 46
odd_week = bool(week%2)
even_week = not odd_week

if odd_week:
    add_task(data, Day.Wednesday, Person.Rolf, mk_food_task(col_R, "RKCHAS"))
    add_task(data, Day.Sunday, Person.Rolf, mk_food_task(col_R, "RKCHAS"))
if even_week:
    add_task(data, Day.Friday, Person.Rolf, mk_food_task(col_R, "RKCHAS"))
add_task(data, Day.Saturday, Person.Rolf, mk_simple_task("Stoevsuge"))

add_task(data, Day.Monday, Person.Karen, mk_simple_task("Vasketoej"))
add_task(data, Day.Tuesday, Person.Karen, mk_simple_task("Vasketoej"))
add_task(data, Day.Wednesday, Person.Karen, mk_simple_task("Vasketoej"))
add_task(data, Day.Thursday, Person.Karen, mk_simple_task("Vasketoej"))
add_task(data, Day.Friday, Person.Karen, mk_simple_task("Vasketoej"))
add_task(data, Day.Saturday, Person.Karen, mk_simple_task("Vasketoej"))
add_task(data, Day.Sunday, Person.Karen, mk_simple_task("Vasketoej"))
add_task(data, Day.Wednesday, Person.Karen, mk_simple_task("Nemlig"))
if even_week:
    add_task(data, Day.Saturday, Person.Karen, mk_food_task(col_K, "RKCHAS"))

add_task(data, Day.Thursday, Person.Cecilia, mk_food_task(col_C, "RKCHAS"))
add_task(data, Day.Saturday, Person.Cecilia, mk_simple_task("Toilet"))
add_task(data, Day.Monday, Person.Cecilia, mk_simple_task("Toemme opvask"))
add_task(data, Day.Tuesday, Person.Cecilia, mk_simple_task("Toemme opvask"))
add_task(data, Day.Wednesday, Person.Cecilia, mk_simple_task("Toemme opvask"))
add_task(data, Day.Thursday, Person.Cecilia, mk_simple_task("Toemme opvask"))
add_task(data, Day.Friday, Person.Cecilia, mk_simple_task("Toemme opvask"))
add_task(data, Day.Saturday, Person.Cecilia, mk_simple_task("Toemme opvask"))
add_task(data, Day.Sunday, Person.Cecilia, mk_simple_task("Toemme opvask"))

if even_week:
    add_task(data, Day.Sunday, Person.Helena, mk_food_task(col_H, "RKCHAS"))
add_task(data, Day.Saturday, Person.Helena, mk_simple_task("Badevaerelse"))

add_task(data, Day.Tuesday, Person.Adam, mk_food_task(col_A, "RKCHAS"))
add_task(data, Day.Wednesday, Person.Adam, mk_simple_task("Lille stoevsugning"))
add_task(data, Day.Monday, Person.Adam, mk_simple_task("Rydde op koekken"))
add_task(data, Day.Tuesday, Person.Adam, mk_simple_task("Rydde op koekken"))
add_task(data, Day.Wednesday, Person.Adam, mk_simple_task("Rydde op koekken"))
add_task(data, Day.Thursday, Person.Adam, mk_simple_task("Rydde op koekken"))
add_task(data, Day.Friday, Person.Adam, mk_simple_task("Rydde op koekken"))
add_task(data, Day.Saturday, Person.Adam, mk_simple_task("Rydde op koekken"))
add_task(data, Day.Sunday, Person.Adam, mk_simple_task("Rydde op koekken"))

add_task(data, Day.Monday, Person.Samuel, mk_food_task(col_S, "RKCHAS"))
add_task(data, Day.Tuesday, Person.Samuel, mk_simple_task("Fodbold kl 16:30"))
add_task(data, Day.Thursday, Person.Samuel, mk_simple_task("Fodbold kl 16:30"))
add_task(data, Day.Friday, Person.Samuel, mk_simple_task("Fodbold kl 15:00"))
add_task(data, Day.Monday, Person.Samuel, mk_simple_task("Feje koekken"))
add_task(data, Day.Tuesday, Person.Samuel, mk_simple_task("Feje koekken"))
add_task(data, Day.Wednesday, Person.Samuel, mk_simple_task("Feje koekken"))
add_task(data, Day.Thursday, Person.Samuel, mk_simple_task("Feje koekken"))
add_task(data, Day.Friday, Person.Samuel, mk_simple_task("Feje koekken"))
add_task(data, Day.Saturday, Person.Samuel, mk_simple_task("Feje koekken"))
add_task(data, Day.Sunday, Person.Samuel, mk_simple_task("Feje koekken"))

def make_field_table(field):
    if field == []:
        return ""
    data = []
    for i in field:
        data.append([i[0]])
    subtable = Table(data)

    subtable.setStyle(TableStyle([
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           ('LEFTPADDING',(0,0),(-1,-1), 0),
                           ('RIGHTPADDING',(0,0),(-1,-1), 0),
                           ('TOPPADDING',(0,0),(-1,-1), 0),
                           ('BOTTOMPADDING',(0,0),(-1,-1), 0)
                           ]))
    return subtable
    if isinstance(field,  tuple):
        return field[0]
    if isinstance(field,  str):
        return field

for day in range(0,7):
    for person in range(0,6):
        data[day+1][person+1] = make_field_table(fields[day][person])

b = Table(data, colWidths=[day_width,human_width,human_width,human_width,human_width,human_width,human_width],
        rowHeights=[30, day_height, day_height, day_height, day_height, day_height, day_height, day_height])
b.hAlign = "LEFT"
b.setStyle(TableStyle([
                           ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
                           ('BACKGROUND',(0,0),(0,-1),HexColor("#C0C0C0")),
                           ('VALIGN',(0,0),(-1,-1),"TOP"),
                           #('BACKGROUND',(2,2),(3,3),HexColor("#f0C0C0")),
                           ('LEFTPADDING',(0,0),(-1,-1), 0),
                           ('RIGHTPADDING',(0,0),(-1,-1), 0),
                           ('TOPPADDING',(0,0),(-1,-1), 0),
                           ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                           ('GRID',(0,0),(-1,-1),1,(0,0,0,)),
                           #('BOX', (2,2), (3,3), 6, HexColor("#00FF00"))
                           ('FONT', (0,0), (0,0), 'Helvetica-Bold')
                           ]))
Story.append(b)

doc.build(Story)
