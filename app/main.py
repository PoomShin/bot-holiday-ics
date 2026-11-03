import sys
from datetime import datetime

import requests as requests
from icalendar import Calendar, Event


# func to fetch calendar data 
def get_calendar(year_no: int) -> dict[datetime, str]:
    url = f"https://bot.or.th.{year_no}.json"

    page = requests.get(url)
    content = page.json()["holidayCalendarLists"]

    output = {}

    for item in content:
        description = item["holidayDescription"].strip()
        date_no = item["date"].split(" ")[-1].strip()
        month = item["month"].strip()
        
        # แก้ไขจุดนี้: บังคับใช้ปีที่ระบุ (2027) แทนข้อมูลดิบในไฟล์ JSON 
        # เพื่อหลีกเลี่ยงข้อผิดพลาดเนื่องจากฝั่ง ธปท. ส่งข้อมูลเก่าปี 2026/2023 กลับมา
        year = str(year_no)

        parsed_date = datetime.strptime(f"{date_no} {month} {year}", "%d %B %Y").date()
        output[parsed_date] = description

    return output


def generate_uid(date: datetime) -> str:
    return f"BOT-{date.strftime('%Y%m%d')}"


if __name__ == "__main__":
    # บังคับล็อคเป้าหมายเป็นปี 2027 
    year = 2027

    # get calendar data
    data = get_calendar(year)

    # create calendar
    cal = Calendar()
    cal.add("prodid", "-//Thai Bank Holiday//NONSGML v1.0//EN")
    cal.add("version", "2.0")

    # add holidays to calendar
    for date, summary in data.items():
        event = Event()
        event.add("summary", summary)
        event.add("dtstart", date)
        event.add("dtend", date)
        event.add("dtstamp", datetime.now())
        event.add("uid", generate_uid(date))
        cal.add_component(event)

    # write calendar to file
    with open("thai bank holidays.ics", "wb") as f:
        f.write(cal.to_ical())
