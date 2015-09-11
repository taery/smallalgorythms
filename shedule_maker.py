__author__ = 'alavrenko'

from icalendar import Calendar, Event
import re

title = 'Погружение в СУБД'
course_id = '157'
course = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/titles.xml', 'r')
tag = re.compile(r'<[^>]+>')
weeks = [tag.sub('', line).strip()[3:] for line in course if 'toggle__title__btn' in line]
print("Load", len(weeks), "items")
course.close()

g = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/my_schedule.ics', 'r')

courseCalendar = Calendar()
courseCalendar.add('prodid', '-//' + title + '//')
courseCalendar.add('version', '2.0')

gcal = Calendar.from_ical(g.read())
g.close()
for component in gcal.walk():
    if component.name == "VEVENT":

        summary = component.get('summary')
        splited_summary = summary.split('"')
        if splited_summary[1] in weeks:
            print(splited_summary)
            print(summary)
            event = Event()
            event.add('summary', summary)
            event.add('dtstart', component.get('dtstart'))
            event.add('dtend', component.get('dtend'))
            event.add('dtstamp', component.get('dtstamp'))
            if 'Module starts' in splited_summary[0]:
                event.add('categories', 'Red Category')
            courseCalendar.add_component(event)

f = open('/Users/alavrenko/Work/from_windows/PycharmProjects/educate/course_' + course_id + '.ics', 'wb')
f.write(courseCalendar.to_ical())
f.close()
