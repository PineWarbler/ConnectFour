# ConnectFour
### A Grove City College Robotics Club project

## Project Goals
- to create a robot that plays Connect Four at a high skill level against a human opponent.  
- Ideally is able to reliably beat its human opponents with minimal algorithm compute time (less than 10s per turn decision).

## ToDo
- [ ] Get H-bridge stepper motor circuit running with Python code
- [ ] finalize and 3d print column-style piece dispenser
- [ ] 3d print and assemble gantry
- [ ] Develop color thresholding algorithm instead of using ArUco codes for locating pieces within the board (?)
    - use HSV colorspace(?)
- [x] Get RPi camera running
- [x] Solve problem of RPi slow minimax compute time (see [BTCommFunctions](/Python/BTCommFunctions.py) that uses wireless Python bluetooth sockets to communicate with a more powerful laptop in about 0.2 seconds per query)

[The GNU General Public License v3.0](LICENSE) Copyright © 2022 Peter Reynolds and the Grove City Robotics Club
