import subprocess

import pprint

metrics_mapping = {
    "System Power": 'power.system',
    "Proc0 Power": 'power.cpu0',
    "Proc1 Power": 'power.cpu1',
    "GPU Power": 'power.gpu',
    "PCIE Proc0 Pwr": 'power.pci0',
    "PCIE Proc1 Power": 'power.pci1',
    "Mem Proc0 Pwr": 'power.mem0',
    "Mem Proc1 Pwr": 'power.mem1',
    "Mem Cache Power": 'power.memcache',
    "Fan Power": 'power.fan',
}

def ipmiapi():
    cmd = ['sudo', 'ipmitool', '-I', 'usb', 'sensor', 'reading']
    cmd += ["System Power", "Proc0 Power", "Proc1 Power", 
            "GPU Power", "PCIE Proc0 Pwr", "PCIE Proc1 Power", 
            "Mem Proc0 Pwr","Mem Proc1 Pwr", "Mem Cache Power", "Fan Power"]
    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out_str = sp.communicate()
    out_list = out_str[0].split('\n')

    out_dict = {}

    for item in out_list:
        try:
            key, val = item.split('|')
            key, val = key.strip(), val.strip()
            out_dict[metrics_mapping[key]] = float(val)
        except:
            pass
    return out_dict

if __name__ == '__main__':
    pprint.pprint(ipmiapi())
