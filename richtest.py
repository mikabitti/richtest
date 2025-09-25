from rich.live import Live
from rich.panel import Panel
from rich.console import Console
from rich import print
from rich.logging import RichHandler
import logging
import time

file_handler = logging.FileHandler("rich_log.log", mode="w")
file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S"))

logging.basicConfig(
    level=logging.NOTSET,
    format="%(message)s",
    datefmt="[%H:%M:%S]",
    handlers=[
        RichHandler(rich_tracebacks=True),
        file_handler
    ]
)

console = Console()

STEP_SIZE = 5

# Your persistent status information

persistent_status_text = ""


def add_step_info_line(current_step):
    global persistent_status_text
    timestamp = time.strftime('%H:%M:%S')
    persistent_status_text = persistent_status_text + \
        f"\n[bold]{current_step}[/bold] steps completed at {timestamp}"


def create_status_panel(current_step, total_items, errors):

    global persistent_status_text

    status_text = f"""
Status: Processing step {current_step}
Items processed: {total_items}
Errors: {errors}
Time: {time.strftime('%H:%M:%S')}
"""

    if persistent_status_text:
        status_text += "\n" + persistent_status_text

    return Panel(status_text, title="Current Status", border_style="blue")


# Example usage
with Live(create_status_panel(0, 0, 0), refresh_per_second=4) as live:

    log = logging.getLogger("rich")

    for i in range(100):
        # Update the persistent display
        live.update(create_status_panel(i, i*10, i//20))

        # Regular prints still work and scroll below
        print(f"Processing item {i}: doing some work...")
        print(f"  - Sub-task completed")
        log.info(f"Logging info for item {i}")
        time.sleep(0.5)

        if i % STEP_SIZE == 0 and i != 0:
            add_step_info_line(i)
