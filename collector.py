import psutil,socket,fcntl,struct,os,time
import requests
from subprocess import check_output
from re import findall
#=================================================
#------- Declaration: Local Variables
#=================================================
url_string = 'http://192.168.0.16:8086/write?db=servers'
networkAdaptor= "eth0"
#=================================================
#------- Functions
#=================================================
def get_uptime():
    uptime = float(os.popen("awk '{print $1}' /proc/uptime").readline())
    return str(time.strftime("%d-day(s) %H:%M:%S", time.gmtime(uptime)))

def get_seconds_elapsed():
    return time.time() - psutil.boot_time()

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])

def get_ip_address(ifname='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def getMAC(interface='eth0'):
  # Return the MAC address of the specified interface
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]

def get_human_readable_size(num):
    exp_str = [ (0, 'B'), (10, 'KB'),(20, 'MB'),(30, 'GB'),(40, 'TB'),(50, 'PB'),]
    i = 0
    while i+1 < len(exp_str) and num >= (2 ** exp_str[i+1][0]):
        i += 1
        rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
    return '%s %s' % (int(rounded_val), exp_str[i][1])
    
#=================================================
#------ Main Code
#=================================================
debugOn=True
if debugOn:
    print(get_uptime())
    print(get_seconds_elapsed())
    print(getMAC(networkAdaptor))
    print(get_ip_address(networkAdaptor))
    print(socket.gethostname())
    print(get_temp())
    print (psutil.cpu_percent(interval=1))
    print (psutil.virtual_memory().percent)
    print (psutil.disk_usage('/').percent)
    print (get_human_readable_size(psutil.virtual_memory().total))

while True:
        C_data = "cpu,host=" + socket.gethostname() + \
                " cpu_percent=" + str(psutil.cpu_percent(interval=1)) + \
                ",cpu_temp=" + str(get_temp())

        S_data = "storage,host=" + socket.gethostname() + \
                " memory_usage_percent=" + str(psutil.virtual_memory().percent) + \
                ",storage_usage_percent=" + str(psutil.disk_usage('/').percent)
        
        E_data = "uptime,host=" + socket.gethostname() + \
                " seconds=" + str(get_seconds_elapsed())

        s = requests.Session()
        s.headers.update({'Content-type':'application/json'})
        try:
                r = s.post(url_string,C_data)
                if debugOn:
                        print("Trying to Send C_data")
                        print(r.status_code)
                        print(r.text)
        except:
                if debugOn:
                        print("unable to send C_data")

        try:
                r = s.post(url_string,S_data)
                if debugOn:
                        print("Trying to Send S_data")
                        print(r.status_code)
                        print(r.text)
        except:
                if debugOn:
                        print("unable to send S_data")
        try:
                r = s.post(url_string,E_data)
                if debugOn:
                        print("Trying to Send E_data")
                        print(r.status_code)
                        print(r.text)
        except:
                if debugOn:
                        print("unable to send E_data")

        time.sleep(5)
