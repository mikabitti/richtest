from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
import time
import threading
from collections import deque

console = Console()


class TopStatusDisplay:
    def __init__(self, max_log_lines=20):
        self.status_info = {
            'operation': 'Starting...',
            'processed': 0,
            'errors': 0,
            'start_time': time.time()
        }
        self.log_buffer = deque(maxlen=max_log_lines)
        self.layout = Layout()

        self.size = 10  # Height of the status panel

        # Split layout: status on top, logs below
        self.layout.split_column(
            Layout(name="status", size=self.size),
            Layout(name="logs", ratio=1)
        )

    def update_status(self, **kwargs):
        self.status_info.update(kwargs)

    def log(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.log_buffer.append(f"[{timestamp}] {message}")

    def get_layout(self):
        # Status panel
        elapsed = time.time() - self.status_info['start_time']
        status_panel = Panel(
            f"Operation: {self.status_info['operation']}\n"
            f"Processed: {self.status_info['processed']} items\n"
            f"Errors: {self.status_info['errors']}\n"
            f"Elapsed: {elapsed:.1f}s",
            title="Status",
            border_style="green"
        )

        # Logs
        log_text = Text("\n".join(self.log_buffer))

        self.layout["status"].update(status_panel)
        self.layout["logs"].update(log_text)

        return self.layout

# Usage


def main():
    display = TopStatusDisplay()

    with Live(display.get_layout(), refresh_per_second=4, screen=True) as live:
        for i in range(100):
            # Update status
            display.update_status(
                operation=f"Processing batch {i}",
                processed=i * 5,
                errors=i // 15
            )

            # Add logs (these will scroll in the bottom section)
            display.log(f"Starting batch {i}")
            display.log(f"  Loading data for batch {i}")
            display.log(f"  Processing {5} items")

            live.update(display.get_layout())
            time.sleep(0.2)


if __name__ == "__main__":
    main()
