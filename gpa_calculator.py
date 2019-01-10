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
        total_credits, gpa = self.calculate_gpa_and_credits(year, semester)
        print('\t\tTotal Credits: {}\tSemester GPA: {}'.format(gpa, total_credits))

    def calculate_gpa_and_credits(self, year, semester):
        total_points = 0
        total_credits = 0
        for course in self.gpa_data[year][semester]:
            total_points += int(course[2]) * GpaFile.gradeValue[course[3]]
            total_credits += int(course[2])
        if total_credits == 0:
            return 0, 0
        return total_credits, round(total_points / total_credits, 2)

    def edit_semester(self, year, semester):
        action = None
        while action != 'b':
            self.show_grades(year, semester)
            print('-' * 70)
            action = input("Add course[A] Edit course[E] Delete course[D] Back[B]: ").lower()
            if action == 'a':
                new_course_name = input('Enter new course name: ')
                new_credits = input("Enter course's credits: ")
                new_grade = input("Enter course's grade: ")
                self.gpa_data[year][semester].append([len(self.gpa_data[year][semester]) + 1,
                                                      new_course_name, new_credits, new_grade])
            if action == 'e':
                course_no = int(input('Select course[Number]: ')) - 1
                print('Edit course [' + self.gpa_data[year][semester][course_no][1] + ']')
                work = None
                course_action = input('Edit course Name[N] or Credits[C] or Grade[G]: ').lower()
                if course_action == 'n':
                    work = ['name', 1]
                elif course_action == 'c':
                    work = ['credits', 2]
                elif course_action == 'g':
                    work = ['grade', 3]
                if work is not None:
                    temp_course_data = input('New course ' + work[0] +
                                             ' [' + self.gpa_data[year][semester][course_no][work[1]] + ']: ') \
                                       or self.gpa_data[year][semester][course_no][work[1]]
                    self.gpa_data[year][semester][course_no][1] = temp_course_data
            if action == 'd':
                course_no = int(input('Select course[Number]: ')) - 1
                del self.gpa_data[year][semester][course_no]
                for i in range(len(self.gpa_data[year][semester])):
                    self.gpa_data[year][semester][i][0] = i + 1

    def insert_semester(self, year, semester):
        self.create_grades_dict(year, semester)
        self.edit_semester(year, semester)

    def delete_semester(self, year, semester):
        del self.gpa_data[year][semester]

    def save_csv(self, filename=None):
        csv_file = open(filename, 'w', newline='')
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for year in self.gpa_data.keys():
            for semester in self.gpa_data[year].keys():
                csv_writer.writerow(['ปีการศึกษา {} ภาคการศึกษาที่ {}'.format(year, semester), '', '', ''])
                csv_writer.writerow(['ลำดับ', 'วิชา', 'หน่วยกิต', 'เกรด'])
                for course in self.gpa_data[year][semester]:
                    # print(course)
                    csv_writer.writerow(course)
                total_credits, gpa = self.calculate_gpa_and_credits(year, semester)
                csv_writer.writerow(['หน่วยกิตที่ได้ประจำภาค', '', total_credits, '', ])
                csv_writer.writerow(['เกรดเฉลี่ยประจำภาค', '', gpa, '', ])
        csv_file.close()


def get_filename():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter CSV Filename: ")
        # filename = 'csv_files/GPA.csv'
    return filename


def input_handler(action, filename):
    if action == 's':
        gpa.save_csv(filename)
        return
    elif action == 'a':
        filename = input("Enter new filename: ")
        gpa.save_csv(filename)
        return
    elif action == 'q':
        return
    try:
        year = int(input('Enter year: '))
        semester = int(input('Enter semester: '))
        print('\n\n')
        if action == 'v':
            gpa.show_grades(year, semester)
        elif action == 'e':
            gpa.edit_semester(year, semester)
        elif action == 'i':
            gpa.insert_semester(year, semester)
        elif action == 'd':
            gpa.delete_semester(year, semester)
        else:
            raise ValueError
    except ValueError:
        print("Wrong input! Enter again!")
    except KeyError:
        print("Invalid year or semester! Enter again!")
    return


filename = get_filename()
gpa = GpaFile(filename)
action = None
while action != 'q':
    action = input('-' * 70 + '\nEnter action\n'
                   'View Semester[V] Insert Semester[I] \n'
                   'Edit Semester[E] Delete Semester[D] \n'
                   'Save[S] Save As[A] Quit(Q)\n'
                   'Action: ').lower()
    input_handler(action, filename)
