import sys
import datetime
import numpy
from importlib import import_module
import matplotlib.pyplot as plt
import util.building
from dateutil.parser import parse

metricspackage = 'metrics'

def _loadmetric(metric):
    metricsmodule = import_module('%s.%s' % (metricspackage, metric))
    run = getattr(metricsmodule, 'run')
    return run
    

def _plotday(metric, title, x, y_day, y_calculated, y):
    f, axarr = plt.subplots(2, sharex=True)

    f.canvas.set_window_title(metric)

    # Subplot A: Separate data
    axarr[0].set_title(title)
    axarr[0].plot(x, y_day, 'r')
    axarr[0].plot(x, y_calculated, 'g')
    axarr[0].set_ylabel("kWh")

    # Subplot B: Visualization
    axarr[1].plot(x, y, 'r')
    axarr[1].axhline(0, color='black')
    axarr[1].set_ylabel("% change")
    axarr[1].set_xlabel("Time (15 min intervals)")

    plt.show()

def visualize(metric, buildingname, date):
    bid = util.building.getbid(buildingname)

    try:
        # Load the metric and run it
        run = _loadmetric(metric)
        print 'load'
        x, y_day, y_calculated, y_visual = run(bid, date)

        # Plot
        datetime = parse(date)
        title = "%s: %s [red=today, green=metric]" % (buildingname, datetime.strftime("%b %d, %Y (%a)"))
        _plotday(metric, title, x, y_day, y_calculated, y_visual)
    except Exception, msg:
        print msg



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Incorrect usage: python visualize.py [metric] [buildingname] [date (YYYY-MM-DD)]'
    else:
        script, metric, buildingname, date = sys.argv
        visualize(metric, buildingname, date)
