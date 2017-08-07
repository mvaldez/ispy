# ISP Spy Project

Script for monitoring bandwidth speeds for your ISP.  Executes in specified time intervals and outputs results to a csv file.  Script depends on [speedtest](https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py) for speed test execution and results.

## Requirements

* Python 3.4+

### Distribution

    $ python3 setup.py sdist
    
### PIP Install

    $ sudo python3 -m pip install isp-spy-0.1.0.tar.gz
    
### Execution

Executes speed test every 30 minutes writing the results to isp-spy.csv with a header row

    $ ispspy.py --interval 30 --header
    
### References

* [speedtest-cli](https://github.com/sivel/speedtest-cli) Command line interface for testing internet bandwidth using speedtest.net