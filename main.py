import cronus.beat as beat
from cronus.timeout import timeout, TimeoutError
from datadog import statsd
import time
import datetime

from nvapi import nvapi
from ipmiapi import ipmiapi

metrics = {
    'gpu': nvapi,
    'ipmi': ipmiapi,
}

@timeout(60)
def report_metrics():
    for metric in metrics:
        for k, v in metrics[metric]().items():
            statsd.gauge(metric + '.' + k, v)

if __name__ == "__main__":
    report_metrics()
    beat.set_rate(1.0 / 10)
    while beat.true():
        try:
            report_metrics()
        except TimeoutError:
            print "timeout"
        try:
            beat.sleep()
        except:
            pass
        print datetime.datetime.now()



