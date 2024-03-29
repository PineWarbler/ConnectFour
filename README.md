# ConnectFour
### A Grove City College Robotics Club project

## Project Goals
- to create a robot that plays Connect Four at a high skill level against a human opponent.  
- Ideally is able to reliably beat its human opponents with minimal algorithm compute time (less than 10s per turn decision).

## Milestones
- 4/19/2022: Our robot beat a human player for the first time (running search depth 4)!

## ToDo
- [ ] revise and print piece dispenser design to have a smaller column
- [ ] solve problem of ridged token edges that prevent clean dispensing
- [ ] Get H-bridge stepper motor circuit running with Python code
- [x] finalize and 3d print column-style piece dispenser
- [ ] 3d print and assemble gantry
- [ ] wire routing
- [x] Develop code localization and piece color classification method
    - Done.  See [interpretBoard.py](/Python/interpretBoard.py), which uses HSV color thresholding and board localization using 4 ArUco markers on board edges
- [x] Get RPi camera running
- [x] Solve problem of RPi slow minimax compute time (see [BTCommFunctions.py](/Python/BTCommFunctions.py) that uses wireless Python bluetooth sockets to communicate with a more powerful laptop in about 0.2 seconds per query)
    - switching to a different minimax implementation significantly reduced computation time (see [better_minimax.py](/Python/better_minimax.py))

## Data Dashboard Display
Intended for display at the annual organization fair at GCC in lieu of a functioning piece placement system.  Most importantly, it allows booth visitors to clearly see the column choice chosen by the minimax algorithm when playing a game at the booth.
See [dashboard.py](/Python/dashboard.py) and the [modified main program](/Python/main_prog_with_dashboard.py)
Below is a screenshot of the data dashboard:
![data_dashboard_screenshot](https://user-images.githubusercontent.com/97372919/180309965-9d43e422-878a-409c-845f-9092095b6c6e.JPG)

## System Block Diagram
![System Block Diagram](https://user-images.githubusercontent.com/97372919/165980542-69b3044f-240c-4b37-ad22-39897a98a895.svg)


[The GNU General Public License v3.0](LICENSE) Copyright © 2022 Peter Reynolds and the Grove City Robotics Club
