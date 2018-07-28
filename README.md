# timetodl
simple api to calculate data transfer time

```
$ curl timetodl.boniface.tech\t# this help text

/<speed>/<size> # return time to transfer file of <size> at <speed>
/10mbps/100mb => 10 seconds
/57kbps/123 gigbytes => 3 weeks, 3 days and 23 hours
/2mbitps/2mb => 8 seconds
/5mbit/s/3gb => 1 hour and 20 minutes

add `bit` to the unit of <speed> if necessary (e.g. mbit for megabits)
-bit units are usually used to measure internet speeds,
other units are usually for file transfers.
```
