import common.db
import nagios.nagios_db
from nagios import nagios_db


def get_test_nagios_problem():
    p = nagios.nagios_db.NagiosProblem()
    p.HostName = "sdc-afs1.umd.edu"
    p.ServiceName = "sis1 qa deploy quota"
    p.ProblemKey = p.HostName + "." + p.ServiceName
    p.Attempt = '3/3'
    p.Created = '1613594513'
    p.Duration = ' 2d  4h 52m 52s'
    p.HostIP = '128.8.163.207'
    p.HostName = 'sdc-afs1.umd.edu'
    p.LastCheck = '02-17-2021 15:39:24'
    p.ServiceName = 'sis1 qa deploy quota'
    p.Status = 'WARNING'
    p.StatusInformation = 'Quota warning: d.oit.ah.d.qa.sis1 using 834923 of 1000000 (83.49%) '
    return p