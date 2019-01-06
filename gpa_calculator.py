#! -*- coding: utf-8 -*-
import csv
import re
import sys
from terminaltables import AsciiTable


class GpaFile:
    gradeValue = {'A': 4, 'B+': 3.5, 'B': 3, 'C+': 2.5, 'C': 2, 'D+': 1.5, 'D': 1, 'F': 0}

    def __init__(self, gpa_filename):
        self.gpa_filename = gpa_filename
        self.gpa_file = open(gpa_filename)
        self.reader = csv.reader(self.gpa_file)
        self.gpa_data = {}
        self.get_grades()

    def get_grades(self):
        for row in self.reader:
            match_semester = re.match(r'ปีการศึกษา (\d+) ภาคการศึกษาที่ (\d+)', row[0], re.M)
            if match_semester:
                year = int(match_semester.group(1))
                semester = int(match_semester.group(2))
                self.create_grades_dict(year, semester)
            elif row[0].isnumeric() and isinstance(row[1], str) and row[2].isnumeric() and isinstance(row[3], str):
                self.gpa_data[year][semester].append(row)

    def create_grades_dict(self, year, semester):
        if year not in self.gpa_data.keys():
            self.gpa_data[year] = {}
        self.gpa_data[year][semester] = []

    def show_grades(self, year, semester):
        table_instance = AsciiTable([['No.', 'Course', 'Credits', 'Grade']] + self.gpa_data[year][semester],
                                    title='YEAR {} SEMESTER {}'.format(year, semester))
        table_instance.justify_columns[0] = 'center'
        table_instance.justify_columns[2] = 'center'
        table_instance.justify_columns[3] = 'center'
        print(table_instance.table)
        gpa, total_credits = self.calculate_gpa_and_credits(year, semester)
        print('\t\tTotal Credits GPA: {}\tSemester GPA: {}'.format(gpa, total_credits))

    def calculate_gpa_and_credits(self, year, semester):
        total_points = 0
        total_credits = 0
        for course in self.gpa_data[year][semester]:
            total_points += int(course[2]) * GpaFile.gradeValue[course[3]]
            total_credits += int(course[2])
        return total_credits, round(total_points / total_credits, 2)

    def edit_grades(self, year, semester):
        action = None
        while action != 'b':
            self.show_grades(year, semester)
            action = input("Add course[A] Edit course[E] Delete course[D] Back[B]: ").lower()
            if action == 'e':
                course_no = int(input('Select course[Number]: ')) - 1
                print('Edit course [' + self.gpa_data[year][semester][course_no][1] + ']')
                course_action = input('Edit course Name[N] or Credits[C] or Grade[G]: ').lower()
                if course_action == 'n':
                    new_course_name = input('New course name [' + self.gpa_data[year][semester][course_no][1] + ']: ') \
                                      or self.gpa_data[year][semester][course_no][1]
                    self.gpa_data[year][semester][course_no][1] = new_course_name
                elif course_action == 'c':
                    new_credits = input('New course credits [' + self.gpa_data[year][semester][course_no][2] + ']: ') \
                                      or self.gpa_data[year][semester][course_no][2]
                    self.gpa_data[year][semester][course_no][2] = new_credits
                elif course_action == 'g':
                    new_grade = input('New course grade [' + self.gpa_data[year][semester][course_no][3] + ']: ') \
                                      or self.gpa_data[year][semester][course_no][3]
                    self.gpa_data[year][semester][course_no][3] = new_grade


def get_filename():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # filename = input("Enter Filename: ")
        filename = 'csv_files/GPA.csv'
    return filename


def show_semester_data():
    try:
        year = int(input('Enter year: '))
        semester = int(input('Enter semester: '))
        print('\n\n')
        gpa.show_grades(year, semester)
    except ValueError:
        print("Wrong input! Enter again!")
        show_semester_data()
    except KeyError:
        print("Invalid year or semester! Enter again!")
        show_semester_data()


def edit_semester_data():
    try:
        year = int(input('Enter year: '))
        semester = int(input('Enter semester: '))
        print('\n\n')
        gpa.edit_grades(year, semester)
    except ValueError:
        print("Wrong input! Enter again!")
        edit_semester_data()
    except KeyError:
        print("Invalid year or semester! Enter again!")
        edit_semester_data()


filename = get_filename()
gpa = GpaFile(filename)
action = None
while action != 'q':
    print('-' * 70)
    action = input('View[V] Insert[I] Edit[E] Save[S] Save As[A] Change File(C) Quit(Q): ').lower()
    if action == 'v':
        show_semester_data()
    if action == 'e':
        edit_semester_data()
