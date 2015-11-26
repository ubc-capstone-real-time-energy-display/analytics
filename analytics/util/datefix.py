import sys


"""
Swap day and month

from: 02/01/2014 6:15 PM
to: 01/02/2014 6:15 PM
"""
def swap(date):
    day, month, rest = date.split('/')

    return '%s/%s/%s' % (month, day, rest)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print 'Incorrect usage: python datefix [filename]'
    else:
        filename = sys.argv[1]

        filedata = []
        with open(filename, 'r') as f:
            filedata.append(f.readline())
            for line in f:
                filedata.append(swap(line))

        with open(filename, 'w') as f:
            for line in filedata:
                f.write(line)
