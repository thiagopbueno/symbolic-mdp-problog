1.000::running(c1, 1) :- reboot(c1).
0.050::running(c1, 1) :- not reboot(c1), not running(c1, 0).
0.725::running(c1, 1) :- not reboot(c1), running(c1, 0), not running(c2, 0).
0.950::running(c1, 1) :- not reboot(c1), running(c1, 0), running(c2, 0).
1.000::running(c2, 1) :- reboot(c2).
0.050::running(c2, 1) :- not reboot(c2), not running(c2, 0).
0.650::running(c2, 1) :- not reboot(c2), running(c2, 0), not running(c1, 0), not running(c3, 0).
0.800::running(c2, 1) :- not reboot(c2), running(c2, 0), running(c1, 0),     not running(c3, 0).
0.800::running(c2, 1) :- not reboot(c2), running(c2, 0), not running(c1, 0), running(c3, 0).
0.950::running(c2, 1) :- not reboot(c2), running(c2, 0), running(c1, 0),     running(c3, 0).
1.000::running(c3, 1) :- reboot(c3).
0.050::running(c3, 1) :- not reboot(c3), not running(c3, 0).
0.725::running(c3, 1) :- not reboot(c3), running(c3, 0), not running(c2, 0).
0.950::running(c3, 1) :- not reboot(c3), running(c3, 0), running(c2, 0).