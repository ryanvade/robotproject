__author__ = 'ryanvade'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)

screen.addstr("This is a Sample Curses Script\n\n")
while True:
    event = screen.getch()
    if event == ord("q"): break
    elif event == curses.KEY_UP:
        screen.clear()
        screen.addstr("The User Pressed UP")
    elif event == curses.KEY_DOWN:
        screen.clear()
        screen.addstr("The User Pressed DOWN")
    elif event == curses.KEY_LEFT:
        screen.clear()
        screen.addstr("The User Pressed LEFT")
    elif event == curses.KEY_RIGHT:
        screen.clear()
        screen.addstr("The User Pressed RIGHT")
    elif event == curses.KEY_NPAGE:
        screen.clear()
        screen.addstr("The User Pressed PG DN")
    elif event == curses.KEY_PPAGE:
        screen.clear()
        screen.addstr("The User Pressed PG UP")

curses.endwin()