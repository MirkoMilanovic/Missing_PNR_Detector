# Missing PNR Detector

This is the implementation of the system for the detection of missing PNR-s. PNR is a record locator
that consists of 6 (six) symbols: letters A-Z and numbers 1-9. Next PNR is determined by
incrementing the previous one.
Here are some examples:
● Current PNR: AAAAAA ; Next PNR: AAAAAB
● Current PNR: AAAAAZ ; Next PNR: AAAAB1
● Current PNR: AAAAA9 ; Next PNR: AAAAAA
We need to find all missing PNRs between the two given ones. If we have the last PNR in our
system AAAAAA, and we receive a new one AAAAAD, our system will need to detect
AAAAAB and AAAAAC as the missing PNRs.

###RESOURCE METHOD CHART:

| Resource        | Method | Path    | Parameter    | Status on error             |
| --------------- | ------ | ------- | ------------ | --------------------------- |
| detectPNR-s     | POST   | /detect | PNR1: String | 200: OK                     |
|                 |        |         | PNR2: String | 301: Missing parameters     |
|                 |        |         |              | 302: Wrong parameter length |
|                 |        |         |              | 303: Wrong parameter symbol |
|                 |        |         |              |                             |
| getDetectedPNRs | GET    | /get    | /            | 200: OK                     |

The system is dockerized, so to build and aggregate the output of the Docker container:

`$ sudo docker-compose build`
`$ sudo docker-compose up`

The system gets implemented as a RESTful API on the localhost, port: 5000.

####Tests - pytest

There is a separate "tests" folder with test scripts, that can be run with pytest (requests library needed).

`$ pip3 install pytest`
`$ pip3 install requests`

`$ pytest` - in the destination folder
