import curses
import time
import threading
from queue import Queue


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input

    # Create windows
    height, width = stdscr.getmaxyx()
    status_win = curses.newwin(5, width, 0, 0)
    log_win = curses.newwin(height-5, width, 5, 0)

    log_lines = []

    def add_log(message):
        log_lines.append(message)
        if len(log_lines) > height - 10:
            log_lines.pop(0)

    # Main loop
    for i in range(100):
        # Update status window
        status_win.clear()
        status_win.addstr(0, 0, f"Status: Step {i}")
        status_win.addstr(1, 0, f"Processed: {i*3} items")
        status_win.addstr(2, 0, f"Time: {time.strftime('%H:%M:%S')}")
        status_win.border()
        status_win.refresh()

        # Add to log
        add_log(f"Processing item {i}: some detailed work")
        add_log(f"  - Completed sub-task for item {i}")

        # Update log window
        log_win.clear()
        for idx, line in enumerate(log_lines[-height+10:]):
            if idx < height - 7:
                log_win.addstr(idx, 0, line[:width-1])
        log_win.refresh()

        time.sleep(0.2)

        # Check for 'q' to quit
        if stdscr.getch() == ord('q'):
            break


if __name__ == "__main__":
    curses.wrapper(main)
