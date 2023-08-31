from calendar_management.futbolempresas_scraper import get_calendar_fe
from calendar_management.gcalendar import gcalendar_service, send_event_to_calendar



def main():
    service = gcalendar_service()
    event_info = get_calendar_fe()
    event = send_event_to_calendar(event_info, service)
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
