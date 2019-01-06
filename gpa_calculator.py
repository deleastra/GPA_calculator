#! -*- coding: utf-8 -*-
import csv
import re
import sys
from terminaltables import AsciiTable

gradeValue = {'A': 4, 'B+': 3.5, 'B': 3, 'C+': 2.5, 'C': 2, 'D+': 1.5, 'D': 1, 'F': 0}


class GpaFile:
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
                self.gpa_data[year][semester].append([row[1], row[2], row[3]])

    def create_grades_dict(self, year, semester):
        if year not in self.gpa_data.keys():
            self.gpa_data[year] = {}
        self.gpa_data[year][semester] = []

    def show_grades(self, year, semester):
        table_instance = AsciiTable([['Course', 'Credits', 'Grade']] + self.gpa_data[year][semester],
                                    title='YEAR {} SEMESTER {}'.format(year, semester))
        print(table_instance.table)
        gpa, total_credits = self.calculate_gpa_and_credits(year, semester)
        print('\tTotal Credits GPA: {}\tSemester GPA: {}'.format(gpa, total_credits))

    def calculate_gpa_and_credits(self, year, semester):
        total_points = 0
        total_credits = 0
        for course in self.gpa_data[year][semester]:
            total_points += int(course[1]) * gradeValue[course[2]]
            total_credits += int(course[1])
        return total_credits, round(total_points / total_credits, 2)


def get_filename():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # filename = input("Enter Filename: ")
        filename = 'csv_files/GPA.csv'
    return filename


def enter_semester():
    try:
        year = int(input('Enter year: '))
        semester = int(input('Enter semester: '))
        gpa.show_grades(year, semester)
    except ValueError:
        print("Wrong input! Enter again!")
        enter_semester()
    except KeyError:
        print("Invalid year or semester! Enter again!")
        enter_semester()


gpa = GpaFile(get_filename())
enter_semester()
