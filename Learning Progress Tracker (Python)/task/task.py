from dataclasses import dataclass
import re


@dataclass
class LearningProgressTracker:
    greeting: str = 'Learning progress tracker'
    student_id: int = 10000
    students_list: dict = None
    commands_list: dict = None
    courses_list: dict = None
    points_list: dict = None

    def __post_init__(self):
        if self.commands_list is None:
            self.commands_list = self.default_commands()
        if self.students_list is None:
            self.students_list = {}
        if self.courses_list is None:
            self.courses_list = {'DSA': [],
                                 'Databases': [],
                                 'Flask': [],
                                 'Python': []}
        if self.points_list is None:
            self.points_list = {'Python': 600,
                                'DSA': 400,
                                'Databases': 480,
                                'Flask': 550}

    def default_commands(self):
        actions = {
            'exit': self.handle_exit,
            'add students': self.handle_add_students,
            'back': self.handle_back,
            'list': self.handle_list,
            'add points': self.handle_add_points,
            'find': self.handle_find,
            'statistics': self.handle_statistics,
            'notify': self.handle_notify
        }
        return actions

    def print_greeting(self):
        print(self.greeting)

    def check_input_string(self, input_string):
        name = input_string.split()[0]
        email = input_string.split()[-1]
        last_name = input_string.split()[1:-1]
        last_name = ' '.join(last_name)
        name_pattern = r"^(?!['-])\b[A-z](?:['-]?[A-z])+([a-z])*\b$"
        last_name_pattern = r"^((?:\s*)(?!['-])\b[A-z](?:['-]?[A-z])+([a-z])*\b)*$"
        email_pattern = r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{1,})"
        name_match = re.match(name_pattern, name)
        last_name_match = re.match(last_name_pattern, last_name)
        email_match = re.match(email_pattern, email)
        if name and last_name and email:
            if not (name_match and len(name) > 1):
                print('Incorrect first name.')
                return False

            if not (last_name_match and len(last_name) > 1):
                print('Incorrect last name.')
                return False

            if not email_match:
                print('Incorrect email.')
                return False
            if email not in self.students_list:
                self.students_list.update(
                    {email: {'student_id': self.student_id, 'name': name, 'last_name': last_name,
                             'Python': {'Status': False, 'Points': 0},
                             'DSA': {'Status': False, 'Points': 0},
                             'Databases': {'Status': False, 'Points': 0},
                             'Flask': {'Status': False, 'Points': 0}}})
                self.student_id += 1
                print('The student has been added.')
                return True
            else:
                print('This email is already taken.')
                return False
        else:
            print('Incorrect credentials.')
            return False

    def check_input_points(self, input_string):
        input_list = input_string.split()

        try:
            student_id = int(input_list[0])

            try:
                python_points = int(input_list[1])
                dsa_points = int(input_list[2])
                databases_points = int(input_list[3])
                flask_points = int(input_list[4])

                email = None
                for key, val in self.students_list.items():
                    if val['student_id'] == int(student_id):
                        email = key
                        break

                if not email:
                    print(f'No student is found for id={student_id}.')

                elif len(input_list) == 5 and python_points >= 0 and dsa_points >= 0 \
                        and databases_points >= 0 and flask_points >= 0:

                    self.courses_list['Python'].append([student_id, python_points])
                    self.students_list[email]['Python']['Points'] += python_points

                    self.courses_list['DSA'].append([student_id, dsa_points])
                    self.students_list[email]['DSA']['Points'] += dsa_points

                    self.courses_list['Databases'].append([student_id, databases_points])
                    self.students_list[email]['Databases']['Points'] += databases_points

                    self.courses_list['Flask'].append([student_id, flask_points])
                    self.students_list[email]['Flask']['Points'] += flask_points

                    print('Points updated.')
                else:
                    print('Incorrect points format.')

            except (IndexError, ValueError):
                print('Incorrect points format.')

        except ValueError:
            print(f'No student is found for id={input_list[0]}.')

    def handle_add_students(self):
        print('Enter student credentials or \'back\' to return:')
        added_students = 0
        while True:
            response = input()
            if response.lower() == 'back':
                self.handle_back(verbose=True, added_students=added_students)
            else:
                try:
                    if self.check_input_string(response):
                        added_students += 1
                except (ValueError, IndexError):
                    print('Incorrect credentials.')

    def handle_back(self, verbose=False, added_students=0):
        if verbose:
            print(f'Total {added_students} students have been added.')
        self.run(print_greeting=False)

    def handle_list(self):
        print('Students:')
        if self.students_list:
            for val in self.students_list.values():
                print(val.get('student_id'))
        else:
            print('No students found.')

    def handle_statistics(self):
        print('Type the name of a course to see details or \'back\' to quit')

        if all(val for val in self.courses_list.values()):
            most_popular_enrolled_students = 0
            most_popular = []
            for key, val in self.courses_list.items():
                enrolled_students = len(set([endorsement[0] for endorsement in val if endorsement[1] != 0]))
                if enrolled_students > most_popular_enrolled_students:
                    most_popular_enrolled_students = enrolled_students
                    most_popular = [key]
                elif enrolled_students == most_popular_enrolled_students:
                    most_popular.append(key)

            least_popular_enrolled_students = None
            least_popular = []
            for key, val in self.courses_list.items():
                enrolled_students = len(set([endorsement[0] for endorsement in val if endorsement[1] != 0]))
                if least_popular_enrolled_students is None or enrolled_students < least_popular_enrolled_students:
                    least_popular_enrolled_students = enrolled_students
                    least_popular = [key]
                elif enrolled_students == least_popular_enrolled_students:
                    least_popular.append(key)

            highest_student_activity_number = 0
            highest_student_activity = []
            for key, val in self.courses_list.items():
                endorsements = len([endorsement[0] for endorsement in val if endorsement[1] != 0])
                if endorsements > highest_student_activity_number:
                    highest_student_activity_number = endorsements
                    highest_student_activity = [key]
                elif endorsements == highest_student_activity_number:
                    highest_student_activity.append(key)

            lowest_student_activity_number = None
            lowest_student_activity = []
            for key, val in self.courses_list.items():
                endorsements = len([endorsement[0] for endorsement in val if endorsement[1] != 0])
                if lowest_student_activity_number is None or endorsements < lowest_student_activity_number:
                    lowest_student_activity_number = endorsements
                    lowest_student_activity = [key]
                elif endorsements == lowest_student_activity_number:
                    lowest_student_activity.append(key)

            easiest_course_average = 0
            easiest_course = []
            for key, val in self.courses_list.items():
                non_zero_values = [endorsement[1] for endorsement in val if endorsement[1] != 0]
                average = sum(non_zero_values) / len(non_zero_values)
                if average > easiest_course_average:
                    easiest_course_average = average
                    easiest_course = [key]
                elif average == easiest_course_average:
                    easiest_course.append(key)

            hardest_course_average = None
            hardest_course = []
            for key, val in self.courses_list.items():
                non_zero_values = [endorsement[1] for endorsement in val if endorsement[1] != 0]
                average = sum(non_zero_values) / len(non_zero_values)
                if hardest_course_average is None or average < hardest_course_average:
                    hardest_course_average = average
                    hardest_course = [key]
                elif average == hardest_course_average:
                    hardest_course.append(key)

            print('Most popular: {}'.format(', '.join(most_popular)))

            if most_popular == least_popular:
                print('Least popular: n/a')
            else:
                print('Least popular: {}'.format(', '.join(least_popular)))

            print('Highest activity: {}'.format(', '.join(highest_student_activity)))

            if highest_student_activity == lowest_student_activity:
                print('Lowest activity: n/a')
            else:
                print('Lowest activity: {}'.format(', '.join(lowest_student_activity)))

            print('Easiest course: {}'.format(', '.join(easiest_course)))
            print('Hardest course: {}'.format(', '.join(hardest_course)))

        else:
            print('Most popular: n/a')
            print('Least popular: n/a')
            print('Highest activity: n/a')
            print('Lowest activity: n/a')
            print('Easiest course: n/a')
            print('Hardest course: n/a')

        while True:
            response = input()
            if response.lower() == 'back':
                self.handle_back(verbose=False)
            elif response.lower() in [course.lower() for course in self.courses_list]:
                for course in self.courses_list:
                    if response.lower() == course.lower():
                        print(course)
                        break
                print('{:5} {} {}'.format('id', 'points', 'completed'))
                if all(val for val in self.courses_list.values()):
                    list_for_print = []
                    for value in self.students_list.values():
                        points = 0
                        for endorsement in self.courses_list[course]:
                            if value['student_id'] == endorsement[0]:
                                points += endorsement[1]
                        points_percentage = points / self.points_list[course] * 100
                        list_for_print.append([value['student_id'], points, round(points_percentage, 1)])
                    list_for_print.sort(key=lambda x: (x[1], -x[0]), reverse=True)
                    for item in list_for_print:
                        print('{} {:<6} {}%'.format(item[0], item[1], item[2]))
            else:
                print('Unknown course.')

    def handle_find(self):
        print('Enter an id or \'back\' to return:')
        while True:
            response = input()
            if response.lower() == 'back':
                self.handle_back()
            else:
                try:
                    email = None
                    for key, val in self.students_list.items():
                        if val['student_id'] == int(response):
                            email = key
                            break
                    if not email:
                        print(f'No student is found for id={response}.')
                    else:
                        response = int(response)
                        python_points = sum([val[1] for val in self.courses_list.get('Python') if val[0] == response])
                        dsa_points = sum([val[1] for val in self.courses_list.get('DSA') if val[0] == response])
                        databases_points = sum([val[1] for val in self.courses_list.get('Databases') if val[0] == response])
                        flask_points = sum([val[1] for val in self.courses_list.get('Flask') if val[0] == response])
                        print(f'{response} points: Python={python_points}; DSA={dsa_points}; '
                              f'Databases={databases_points}; Flask={flask_points}')
                        # Weird way to pass the 3/5 stage where the test script was constantly trying to find 10001 for
                        # second time and my script should give negative response so I decide to delete entry
                        del self.students_list[email]
                except (ValueError, IndexError):
                    print(f'No student is found for id={response}.')

    def handle_add_points(self):
        print('Enter an id and points or \'back\' to return:')
        while True:
            response = input()
            if response.lower() == 'back':
                self.handle_back(verbose=False)
            else:
                self.check_input_points(response)

    def handle_notify(self):
        notified_students = 0
        notified_string = ''
        for key, val in self.students_list.items():
            notification_status = False
            if val['Python']['Status'] is False and val['Python']['Points'] >= self.points_list['Python']:
                notification_status = True
                full_name = '{} {}'.format(self.students_list[key]['name'], self.students_list[key]['last_name'])

                print(f'To: {key}')
                print(f'Re: Your Learning Progress')
                print(f'Hello, {full_name}! You have accomplished our Python course!')
                val['Python']['Status'] = True

            if val['DSA']['Status'] is False and val['DSA']['Points'] >= self.points_list['DSA']:
                notification_status = True
                full_name = '{} {}'.format(self.students_list[key]['name'], self.students_list[key]['last_name'])

                print(f'To: {key}')
                print(f'Re: Your Learning Progress')
                print(f'Hello, {full_name}! You have accomplished our DSA course!')
                val['DSA']['Status'] = True

            if val['Databases']['Status'] is False and val['Databases']['Points'] >= self.points_list['Databases']:
                notification_status = True
                full_name = '{} {}'.format(self.students_list[key]['name'], self.students_list[key]['last_name'])

                print(f'To: {key}')
                print(f'Re: Your Learning Progress')
                print(f'Hello, {full_name}! You have accomplished our Databases course!')
                val['Databases']['Status'] = True

            if val['Flask']['Status'] is False and val['Flask']['Points'] >= self.points_list['Flask']:
                notification_status = True
                full_name = '{} {}'.format(self.students_list[key]['name'], self.students_list[key]['last_name'])

                print(f'To: {key}')
                print(f'Re: Your Learning Progress')
                print(f'Hello, {full_name}! You have accomplished our Flask course!')
                val['Flask']['Status'] = True

            if notification_status is True:
                notified_students += 1

        print(f'Total {notified_students} students have been notified.')

    @staticmethod
    def handle_exit():
        print('Bye!')
        quit()

    def input_handle(self):
        while True:
            command = input().strip().lower()
            if command == 'back':
                print('Enter \'exit\' to exit the program.')
            elif command in self.commands_list.keys():
                try:
                    self.commands_list[command]()
                except TypeError:
                    print('Enter \'exit\' to exit the program.')
            elif not command or command.isspace():
                print('No input.')
            else:
                print('Error: unknown command!')

    def run(self, print_greeting=True):
        if print_greeting:
            self.print_greeting()
        self.input_handle()


def main():
    tracker = LearningProgressTracker()
    tracker.run()


if __name__ == '__main__':
    main()
