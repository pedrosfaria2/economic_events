import httpx
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_data(url, headers, cookies, data):
    """
    Function to fetch data from a given URL using POST request with specified headers, cookies, and data.
    """
    with httpx.Client(follow_redirects=True, cookies=cookies) as client:
        response = client.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get('data')
        print(f"Failed to get data: {response.status_code}")
        return None

def extract_volatility(cell_html):
    """
    Function to extract the volatility level from the HTML content of a cell.
    """
    if 'High Volatility Expected' in cell_html:
        return 'High'
    if 'Moderate Volatility Expected' in cell_html:
        return 'Moderate'
    if 'Low Volatility Expected' in cell_html:
        return 'Low'
    return None

def parse_html(html_content):
    """
    Function to parse the HTML content and extract economic event data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    events = []
    current_date = None

    for row in soup.find_all(['tr', 'td'], {'class': ['js-event-item', 'theDay']}):
        if 'theDay' in row.get('class', []):
            current_date = row.get_text(strip=True)
        elif 'js-event-item' in row.get('class', []):
            row_html = str(row)
            volatility = extract_volatility(row_html)
            event = {
                'Date': datetime.strptime(current_date, '%A, %B %d, %Y').strftime('%m/%d/%y'),
                'Time': row.find('td', class_='js-time').get_text(strip=True) if row.find('td', class_='js-time') else None,
                'Currency': row.find('td', class_='flagCur').get_text(strip=True) if row.find('td', class_='flagCur') else None,
                'Volatility': volatility,
                'Event': row.find('td', class_='event').get_text(strip=True) if row.find('td', class_='event') else None,
                'Forecast': row.find('td', class_='fore').get_text(strip=True) if row.find('td', class_='fore') else None,
                'Previous': row.find('td', class_='prev').get_text(strip=True) if row.find('td', class_='prev') else None,
            }
            events.append(event)
    return events

def fetch_economic_events():
    """
    Function to fetch economic events for the current and next week from the Investing.com economic calendar.
    """
    url = "https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.investing.com",
        "Pragma": "no-cache",
        "Referer": "https://www.investing.com/economic-calendar/",
        "Sec-CH-UA": '"Not/A;Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {
        "PHPSESSID": "telbckiou16uufp5s2qd09hjsk",
        "geoC": "BR",
        "page_equity_viewed": "0",
        "browser-session-counted": "true",
        "user-browser-sessions": "1",
        "adsFreeSalePopUp": "1",
        "adBlockerNewUserDomains": "1719873801",
        "gtmFired": "OK",
        "nyxDorf": "MzQ%2BZTNlZDw0aGhlNzZkZT5lMTthMjsxMzBlbDE%2FZm0xZmM3b2M1M2MxPmNhaWVhYmRiYj5uYjY0PWI6NmVnNzM1PmczZ2RrNGdobA%3D%3D",
        "udid": "a2bcb6d6a827d4f0c8a40b509bebfc97",
        "smd": "a2bcb6d6a827d4f0c8a40b509bebfc97-1719873800",
        "__cf_bm": "LgiKTZ_0yCSBLMRzRnvQGb.8Ll3Hb4hC6dSRgM0thyY-1719873801-1.0.1.1-rcgh3yYXQAmuR8W.eSdtHNrZnUskd6DtqLHhfuIhr710F72p3rz12awhmqZdXSs.vsiOZ20.fvf6kGlstf2DwDdj9M1zJyYSPD5JpcOOCRE",
        "__cflb": "0H28vY1WcQgbwwJpSw5YiDRSJhpofbxeRRLrHXVwGLk",
        "usprivacy": "1YNN",
        "_gid": "GA1.2.1187722834.1719873897",
        "_imntz_error": "0",
        "cf_clearance": "pMZ1PhsuQCp.DisOWWk0YFPCpXuHdJEM6i0T1xDihSQ-1719873802-1.0.1.1-fCy3zIDGNe1DHIxiBWfmnpbng6c2WoH3AOMkJy2bVnEOmRnUH0UCDGHLYg_QNpizqfw.d_OsQLVr7zZoUyAo4w",
        "_hjSessionUser_174945": "eyJpZCI6IjNiNjFhZTM5LTI1MGQtNWVkZC04ZDJiLTQwZTUxNmNiNDBmNSIsImNyZWF0ZWQiOjE3MTU5MDY2NzkxMjAsImV4aXN0aW5nIjp0cnVlfQ==",
        "_hjSession_174945": "eyJpZCI6IjU2OTk2ZGFhLTkzYWEtNDZjMS04MDdlLTZmNDY5YzhhZjI4YSIsImMiOjE3MTk4NzM4OTc2NjEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=",
        "_ga": "GA1.1.1966211167.1719873897",
        "__eventn_id": "a2bcb6d6a827d4f0c8a40b509bebfc97",
        "OneTrustWPCCPAGoogleOptOut": "false",
        "editionPostpone": "1719873903113",
        "r_p_s_n": "1",
        "reg_trk_ep": "exit popup banner",
        "_cc_id": "4efdbc1d588793a09f80532ba4b8edfe",
        "panoramaId_expiry": "1720478612700",
        "panoramaId": "c56eb0a4c51e0dde4dd50475cca7185ca02c976eb81b2e083e31bb96de376b9e",
        "panoramaIdType": "panoDevice",
        "cto_bundle": "75gbl19UY3V5SWZRWXZJMk0mMExEdUZlWmNBM1gybHRGR2ZGeTB0Uk1rek9LMExyMFhFbFJ6amIwaUZhNzk3cnJncDVRTkZ4NjBoNU9OU2VaNkRwdW1hN0Zjck52U3RpNXZteGxBYTdkTFRYeVNJMFAzUUN5bm1odEpWRG9mMzRGTjE5Rg",
        "gcc": "BR",
        "gsc": "SP",
        "invpc": "2",
        "page_view_count": "2",
        "lifetime_page_view_count": "1",
        "reg_trk_ep": "google%20one%20tap",
        "_hjHasCachedUserAttributes": "true",
        "_ga_C4NDLGKVMK": "GS1.1.1719873897.1.1.1719874719.60.0.0",
        "pm_score": "clear",
    }

    data_this_week = {
        "country[]": [
            "25", "32", "6", "37", "72", "22", "17", "39", "14", "10",
            "35", "43", "56", "36", "110", "11", "26", "12", "4", "5"
        ],
        "timeZone": "8",
        "timeFilter": "timeRemain",
        "currentTab": "thisWeek",
        "limit_from": "0"
    }

    data_next_week = {
        "country[]": [
            "25", "32", "6", "37", "72", "22", "17", "39", "14", "10",
            "35", "43", "56", "36", "110", "11", "26", "12", "4", "5"
        ],
        "timeZone": "8",
        "timeFilter": "timeRemain",
        "currentTab": "nextWeek",
        "limit_from": "0"
    }

    # Fetch data for this week and next week
    html_this_week = fetch_data(url, headers, cookies, data_this_week)
    html_next_week = fetch_data(url, headers, cookies, data_next_week)

    # Parse the HTML content to extract events
    events_this_week = parse_html(html_this_week) if html_this_week else []
    events_next_week = parse_html(html_next_week) if html_next_week else []

    # Combine events from both weeks
    all_events = events_this_week + events_next_week

    return all_events
