import sys
import time


class StatusDisplay:
    def __init__(self, lines=4):
        self.lines = lines
        self.setup()

    def setup(self):
        # Reserve space at top
        for _ in range(self.lines):
            print()
        # Move cursor back up
        sys.stdout.write(f'\033[{self.lines}A')
        sys.stdout.flush()

    def update_status(self, status_text):
        # Save cursor position
        sys.stdout.write('\033[s')
        # Move to top
        sys.stdout.write(f'\033[{self.lines}A')
        # Clear the status area
        for _ in range(self.lines):
            sys.stdout.write('\033[2K\033[1B')
        # Move back to top
        sys.stdout.write(f'\033[{self.lines}A')
        # Write new status
        print(status_text)
        # Restore cursor position
        sys.stdout.write('\033[u')
        sys.stdout.flush()


# Usage
status = StatusDisplay(3)
for i in range(50):
    # Update persistent status
    status.update_status(
        f"Current step: {i}\nItems processed: {i*5}\nErrors: {i//10}")

    # Regular prints
    print(f"Working on item {i}...")
    print(f"  Details about item {i}")

    time.sleep(0.3)
