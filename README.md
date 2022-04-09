# ConnectFour
### A Grove City College Robotics Club project

## Project Goals
- to create a robot that plays Connect Four at a high skill level against a human opponent.  
- Ideally is able to reliably beat its human opponents with minimal algorithm compute time (less than 10s per turn decision).

## ToDo
- [ ] Get H-bridge stepper motor circuit running with Python code
- [x] finalize and 3d print column-style piece dispenser
- [ ] 3d print and assemble gantry
- [x] Develop code localization and piece color classification method
    - Done.  See [interpretBoard.py](/Python/interpretBoard.py), which uses HSV color thresholding and board localization using 4 ArUco markers on board edges
- [x] Get RPi camera running
- [x] Solve problem of RPi slow minimax compute time (see [BTCommFunctions.py](/Python/BTCommFunctions.py) that uses wireless Python bluetooth sockets to communicate with a more powerful laptop in about 0.2 seconds per query)
    - switching to a different minimax implementation significantly reduced computation time (see [better_minimax.py](/Python/better_minimax.py))

[The GNU General Public License v3.0](LICENSE) Copyright © 2022 Peter Reynolds and the Grove City Robotics Club
