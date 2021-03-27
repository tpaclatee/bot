import requests
from bs4 import NavigableString, BeautifulSoup
from requests.auth import HTTPBasicAuth

from common import conf
from nagios.nagios_db import NagiosProblem


def scrape():
    result = requests.get(
        'https://nagios.umd.edu/nagios/cgi-bin/status.cgi?hostgroup=ioc-host&style=detail&servicestatustypes=28&limit'
        '=100&sorttype=1&sortoption=6&start=0&limit=500',
        auth=HTTPBasicAuth(conf.nagios_user, conf.nagios_pass))
    c = result.content
    soup = BeautifulSoup(c, features="lxml")
    table = soup.find('table', attrs={'class': 'status'})
    data = []
    rows = table.contents
    for row in rows:
        if not isinstance(row, NavigableString):
            if not row.find('th'):
                td = row.find('td')
                if td:
                    if not td.attrs.get('colspan') == '6':
                        p = NagiosProblem()
                        cols = row.contents
                        for i in range(len(cols)):
                            if i == 1:
                                parse_host(cols[1], p)
                            elif i == 3:
                                parse_service(cols[3], p)
                            elif i == 5:
                                p.Status = cols[5].text
                            elif i == 7:
                                p.LastCheck = cols[7].text
                            elif i == 9:
                                p.Duration = cols[9].text
                            elif i == 11:
                                p.Attempt = cols[11].text
                            elif i == 13:
                                p.StatusInformation = cols[13].text
                        if not p.HostName:
                            p.ProblemKey = p.ServiceName
                        else:
                            p.ProblemKey = p.HostName + "." + p.ServiceName
                        data.append(p)
    return data


def parse_host(td, p):
    """Parse host cell and icons"""
    table = td.find('table')
    if not table:
        return  # empty host cell
    tr = table.find('tr')
    tds = tr.contents
    for cell in tds:
        host_name_cell = tds[1]
        a = host_name_cell.find('a')
        p.HostIP = a.attrs.get('title')
        p.HostName = a.text
        icons_table = tds[3]
        itr = icons_table.find_all('tr')
        for i in itr:
            img = i.find('img')
            src = img.attrs.get('src')
            if "ack" in src:
                p.AcknowledgedHost = True
            elif "ndisabled" in src:
                p.NotificationDisabledHost = True
            elif "downtime" in src:
                p.ScheduledDowntimeHost = True
            elif "passiveonly" in src:
                p.PassiveChecksOnlyHost = True


def parse_service(td, p):
    """
    Parse service
    """
    table = td.find('table')
    # Debug a specific row
    # if p.HostName:
    #    if 'ditinternal' in p.HostName:
    #        print('here')
    if not table:
        return  # empty host cell
    tr = table.find('tr')
    tds = tr.contents
    service_name_cell = tds[0]
    a = service_name_cell.find('a')
    p.ServiceName = a.text
    for cell in tds:
        icons_table = tds[2].contents
        icons_inner_tab = icons_table[1].contents
        icons_inner_td = icons_inner_tab[1].contents
        for i in icons_inner_td:
            if isinstance(i, NavigableString):
                continue  # skip blank
            img = i.find('img')
            if img:
                src = img.attrs.get('src')
                if "ack" in src:
                    p.AcknowledgedService = True
                elif "ndisabled" in src:
                    p.NotificationDisabledService = True
                elif "downtime" in src:
                    p.ScheduledDowntimeService = True
                elif "passiveonly" in src:
                    p.PassiveChecksOnlyService = True
