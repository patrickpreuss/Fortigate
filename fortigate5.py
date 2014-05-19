#!/usr/bin/env python 

__author__ = 'dwilliams'
import iptools


avaimodels = ['1.  200D', '2.  100D', '3.  90D', '4.  60D', '5.  30D']



template200d = "/usr/local/etc/Fortigate/200d_template"
template100d = "/usr/local/etc/Fortigate/100d_template"
template90d = "/usr/local/etc/Fortigate/90d_template"
template60d = "/usr/local/etc/Fortigate/60d_template"
template30d = "/usr/local/etc/Fortigate/30d_template"

def replace(file, newfile, mydict):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Search and replace using dictionary keys
    for k, v in mydict.iteritems():
        file_string = file_string.replace(k, v)

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(newfile, 'w')
    file_handle.write(file_string)
    file_handle.close()
    print "created file "+hostname+".conf"

def get_dg():
    global extIPandMask
    global defaultgateway
    defaultgateway = raw_input('Default Gateway IP: ')
    r = iptools.IpRangeList(extIPandMask).__contains__(defaultgateway)
    x = extIPandMask.split('/')
    address = x[0]
    if r is False:
        print 'Make sure it is a valid IP within the external IP network'
        get_dg()
    if defaultgateway == address:
        print 'Your gateway cannot be the same as your local IP'
        get_dg()
    else:
        pass

def validateEmail(a):
    sep=[x for x in a if not x.isalpha()]
    sepjoined=''.join(sep)
    ## sep joined must be ..@.... form
    if sepjoined.strip('.') != '@': return False
    end=a
    for i in sep:
        part,i,end=end.partition(i)
        if len(part)<2: return False
    return True


def validate_cidr_mask(s):
    if not s.isdigit():
        print "Invalid or missing cidr mask"
        return False
    i = int(s)
    if i < 1 or i > 32:
        return False
    else:
        return True


def validate_ipv4_format(s):
    a = s.split('.')
    if len(a) != 4:
        print 'Not a Valid IP Address'
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
        return True


def validatemod(s):
    if int(s) > 5:
        print('Invalid Entry')
        return False


def outputipv4(s):
    x = iptools.ipv4.cidr2block(s)
    n = x[0]
    return n


def modselect(model):
    global models
    model = raw_input('Enter Number: ')
    if model == '1':
        return template200d
    elif model == '2':
        return "template100d"
    elif model == '3':
        return "template90d"
    elif model == '4':
        return "template60d"
    elif model == '5':
        return "template30d"
    else:
        v = validatemod(model)
        if v == False:
            modselect(model)
        else:
            pass

def validate_ip_cidr_format(s):
    if iptools.ipv4.validate_cidr(s) == False:
        print "Invalid cidr format"
        getexternalIPMask(i)
    else:
        pass

def validate_int_ip_cidr_format(s):
    if iptools.ipv4.validate_cidr(s) == False:
        print "Invalid cidr format"
        getinternalip()
    else:
        pass

def getexternalIPMask():
    global extIPandMask
    extIPandMask = raw_input('External IP Address and Mask(cidr): ')
    validate_ip_cidr_format(extIPandMask)
    x = extIPandMask.split('/')
    address = x[0]
    cidr = x[1]
    v = validate_ipv4_format(address)
    c = validate_cidr_mask(cidr)
    if v == False:
        getexternalIPMask()
    elif c == False:
        print "Invalid Mask"
        getexternalIPMask()
    else:
        pass


print('Select the number corresponding to the model being provisioned')
for i in avaimodels:
    print i

def getinternalip():
    global intIPandMask
    global internalnet
    intIPandMask = raw_input('Internal IP Address and Mask(cidr): ')
    validate_int_ip_cidr_format(intIPandMask)
    x = intIPandMask.split('/')
    address = x[0]
    cidr = x[1]
    v = validate_ipv4_format(address)
    c = validate_cidr_mask(cidr)
    internalnet = outputipv4(intIPandMask)+'/'+cidr
    if v == False:
        getinternalip()
    elif c == False:
        print "Invalid Mask"
        getinternalip()
    else:
        pass

def getdns1():
    global DNS1
    DNS1 = raw_input('Primary DNS Server IP: ')
    validation = validate_ipv4_format(DNS1)
    if validation == False:
        print 'Not a valid IP address'
        getdns1()
    else:
        pass

def getdns2():
    global DNS2
    DNS2 = raw_input('Secondary DNS Server IP: ')
    validation = validate_ipv4_format(DNS2)
    if validation == False:
        print 'Not a valid IP address'
        getdns2()
    else:
        pass

def getemail():
    global emailaddr
    emailaddr = raw_input('Source Email Address [email@example.com]: ')
    x = validateEmail(emailaddr)
    if x == False:
        print "Email is not formatted properly"
        getemail()
    else:
        pass

def validateEmail(a):
    sep=[x for x in a if not x.isalpha()]
    sepjoined=''.join(sep)
    ## sep joined must be ..@.... form
    if sepjoined.strip('.') != '@': return False
    end=a
    for i in sep:
        part,i,end=end.partition(i)
        if len(part)<2: return False
    return True

templatefile = ()
defaultgateway = ()
extIPandMask = ()
models = ()
intIPandMask = ()
DNS1 = ()
DNS2 = ()
internalnet = ()
emailaddr = ()
models = modselect(models)
hostname = raw_input('Hostname [SID-Profile]: ')
getexternalIPMask()
get_dg()
getinternalip()
getdns1()
getdns2()
NTP1 = DNS1
NTP2 = DNS2
domain = raw_input('Domain name [example.com]: ')
getemail()
password = raw_input('Enter a password containing 1 number, uppercase letter, lowercase letter, and 1 special character: ')
snmpcomm = raw_input('Enter a password to be used as the snmp read community: ')
SID = raw_input('Service ID (SID): ')

if models == "template200d":
    templatefile = template200d
elif models == "template100d":
    templatefile = template100d
elif models == "template90d":
    templatefile = template90d
elif models == "template60d":
    templatefile = template60d
elif models == "template30d":
    templatefile = template30d


repldict = {"#HOSTNAME#":hostname,
"#EXTERNALIPADDRESS#":extIPandMask,
"#InternalIPADDRESS#":intIPandMask,
"#InternalNetwork#":internalnet,
"#DNS1#":DNS1,
"#DNS2#":DNS2,
"#NTP1#":NTP1,
"#NTP2#":NTP2,
"#InternalNetwork2#":internalnet,
"#DOMAIN1#":domain,
"#SRCEMAIL#":emailaddr,
"#DEFAULTGW#":defaultgateway,
"#PASSWORD#":password,
"#snmp_community#":snmpcomm,
"#SID#":SID}




replace(templatefile, hostname+'.conf', repldict)
