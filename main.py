
courses = ['Python', 'Java', 'C++', 'C#']


def average_mark_list_person(l_persons, l_courses='', accuracy=2):
    result = {}

    for l_person in l_persons:
        #print(l_person)
        #print(average_mark_single_person(l_person, l_courses, accuracy))
        result[l_person] = average_mark_single_person(l_person, l_courses, accuracy)

    return result


def average_mark_single_person(l_person, l_courses='', accuracy=2):
    marks_summa = 0
    marks_count = 0
    result = 0

    if 'grades' not in l_person.__dict__:
        return result

    if l_courses == '':
        for v in l_person.grades.values():
            marks_summa += sum(v)
            marks_count += len(v)
    else:
        if type(l_courses) == type(str()):
            l_courses = [l_courses]
        for l_course in l_courses:
            if l_course in l_person.grades:
                marks_summa += sum(l_person.grades[l_course])
                marks_count += len(l_person.grades[l_course])

    if marks_count != 0:
        result = round(marks_summa / marks_count, accuracy)

    return result


class Person:
    def __init__(self, name, surname, gender=''):
        self.name = str(name).capitalize()
        self.surname = str(surname).capitalize()
        self.gender = gender

    def full_name(self):
        return f'{self.name} {self.surname}'


class Student(Person):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за домашние задания: {self._average_mark()}\n' \
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
               f'Завершенные курсы: {", ".join(self.finished_courses)}'

    def __lt__(self, other):
        if isinstance(other, Student):
            return self._average_mark() < other._average_mark()
        else:
            raise Exception(f'Сравнение типов {type(self)} и {type(other)} не определено')

    def _average_mark(self, course='', accuracy=2):
        return average_mark_single_person(self, course, accuracy)

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            print(f'Ошибка выставления оценок. Возможные причины:\n'
                  f'Курс "{course}" не прикреплен к лектору {lecturer.full_name()}\n'
                  f'Студент {self.full_name()} не записан на курс "{course}" или завершил его\n')


class Mentor(Person):
    def __init__(self, name, surname, gender=''):
        super().__init__(name, surname, gender)
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за лекции: {self._average_mark()}'

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self._average_mark() < other._average_mark()
        else:
            raise Exception(f'Сравнение типов {type(self)} и {type(other)} не определено')

    def _average_mark(self, course='', accuracy=2):
        return average_mark_single_person(self, course, accuracy)


class Reviewer(Mentor):
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print(f'Ошибка выставления оценок. Возможные причины:\n'
                  f'Курс "{course}" не прикреплен к эксперту {self.full_name()}\n'
                  f'Студент {student.full_name()} не записан на курс "{course}" или завершил его\n')


# исходные данные
student_Antony = Student('Antony', 'Smith', 'male')
student_Antony.courses_in_progress += [courses[0], courses[1], courses[2]]
student_Antony.finished_courses += [courses[3]]
student_Jinny = Student('Jinny', 'Robson', 'female')
student_Jinny.courses_in_progress += [courses[0], courses[2], courses[3]]
student_Jinny.finished_courses += [courses[1]]

lecturer_Rob = Lecturer('Rob', 'Black')
lecturer_Rob.courses_attached += [courses[0], courses[1]]
lecturer_John = Lecturer('John', 'White')
lecturer_John.courses_attached += [courses[2], courses[3]]

reviewer_Bob = Reviewer('Bob', 'Sparrow')
reviewer_Bob.courses_attached += [courses[0], courses[2]]
reviewer_Tom = Reviewer('Tom', 'Wolf')
reviewer_Tom.courses_attached += [courses[1], courses[3]]

students = [student_Antony, student_Jinny]
lecturers = [lecturer_Rob, lecturer_John]
reviewers = [reviewer_Bob, reviewer_Tom]

# изменение оценок

reviewers[0].rate_hw(students[0], 'Python', 10)
reviewers[0].rate_hw(students[1], 'C++', 8)
reviewers[1].rate_hw(students[0], 'Java', 9)
students[0].rate_hw(lecturers[0], 'Java', 7)
students[0].rate_hw(lecturers[1], 'C++', 10)
students[1].rate_hw(lecturers[1], 'C#', 9)
students[1].rate_hw(lecturers[1], 'C++', 9)
students[1].rate_hw(lecturers[0], 'Python', 10)

# print
print('')
print('СТУДЕНТЫ:')
for person in students:
    print('')
    print(person)

print('')
print('ЛЕКТОРЫ:')
for person in lecturers:
    print('')
    print(person)

print('')
print('ЭКСПЕРТЫ:')
for person in reviewers:
    print('')
    print(person)

# for course in courses:
#     print('grades' in reviewers[0].__dict__)

print('')
print('СРАВНЕНИЕ СТУДЕНТОВ:')
print(f'Студент {students[0].full_name()} меньше студента {students[1].full_name()}: {students[0] < students[1]}')

print('')
print('СРАВНЕНИЕ ЛЕКТОРОВ:')
print(f'Лектор {lecturers[0].full_name()} меньше лектора {lecturers[1].full_name()}: {lecturers[0] < lecturers[1]}')

# Оценки по курсам

l_courses = [[courses[0], courses[2]], courses, [courses[1]]]
for c in l_courses:
    print('')
    print(f'СРЕДНИЕ ОЦЕНКИ за курсы {", ".join(c)}:')

    for key, value in average_mark_list_person(students, c).items():
        print(key.full_name(), value)

    for key, value in average_mark_list_person(lecturers, c).items():
        print(key.full_name(), value)
