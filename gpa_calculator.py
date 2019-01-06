#! -*- codding: utf-8 -*-
import csv


class GpaFile:
    def __init__(self, gpa_filename):
        self.gpa_filename = gpa_filename
        self.gpa_file = open(gpa_filename)
        self.reader = csv.reader(self.gpa_file)


# filename = input("Enter Filename: ")
filename = 'D:\Download\MY GPA - GPA_for_CSV (1).csv'
gpa = GpaFile(filename)
