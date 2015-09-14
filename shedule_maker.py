__author__ = 'alavrenko'

from icalendar import Calendar, Event
import re

title = 'Погружение в СУБД'
course_id = '157'
course = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/titles_157.xml', 'r')

# title = 'Основы теории графов'
# course_id = '126'
# course = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/titles_126.xml', 'r')

# title = 'Основы перечислительной комбинаторики'
# course_id = '125'
# course = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/titles_125.xml', 'r')

# title = 'Функциональное программирование'
# course_id = '75'
# course = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/titles_75.xml', 'r')

# title = 'Развитие рационального интеллекта'
# course_id = '131'
# course = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/titles_131.xml', 'r')

# title = 'Алгоритмы: теория и практика'
# course_id = '218'
# course = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/titles_218.xml', 'r')

tag = re.compile(r'<[^>]+>')
weeks = {tag.sub('', line).strip()[3:]: tag.sub('', line).strip()[:1] for line in course if 'toggle__title__btn' in line}
print("Load", len(weeks), "items")
print('\n'.join(weeks))
course.close()

course_url = 'http://www.stepic.org/course/' + str(course_id) + '/syllabus?section='

g = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/my_schedule.ics', 'r')

courseCalendar = Calendar()
courseCalendar.add('prodid', '-//' + title + '//')
courseCalendar.add('version', '2.0')

gcal = Calendar.from_ical(g.read())
g.close()
test = dict()
skipHardDeadlines = False
for component in gcal.walk():
    if component.name == "VEVENT":
        summary = component.get('summary')
        splited_summary = [_.strip() for _ in summary.split('"')]
        # print(splited_summary)
        if splited_summary[1] in weeks:
            if 'Soft deadline for module' in splited_summary[0]:
                skipHardDeadlines = True
            if splited_summary[1] not in test:
                test[splited_summary[1]] = []
            test[splited_summary[1]].append(component)
print("Find", len(test), "modules")
for module in test:
    event = Event()
    event.add('summary', module)
    print("Adding event", module)
    events = test[module]
    print("Load", len(events), "events")
    if len(events) == 1:
        print("Add single event")
        event.add('dtstart', events[0].get('dtstart'))
        event.add('dtend', events[0].get('dtend'))
        event.add('url', course_url + weeks[module])
    else:
        for e in events:
            splited_summary = e.get('summary').split('"')
            if 'Module starts' in splited_summary[0]:
                print("Add starting event")
                event.add('dtstart', e.get('dtstart'))
                event.add('url', course_url + weeks[module])
            elif 'Soft deadline for module' in splited_summary[0]:
                print("Add finishing event, hard deadline will be skiped")
                event.add('dtend', e.get('dtend'))
            elif 'Hard deadline for module' in splited_summary[0] and not skipHardDeadlines:
                print("Add finishing event")
                event.add('dtend', e.get('dtend'))

    courseCalendar.add_component(event)

f = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/course_' + course_id + '.ics', 'wb')
f.write(courseCalendar.to_ical())
f.close()
