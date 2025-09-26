from rich.live import Live
from rich.panel import Panel
from rich.console import Console
from rich import print
from rich.logging import RichHandler
import logging
import time

# Setup logging (same as your original)
file_handler = logging.FileHandler("rich_log.log", mode="w")
file_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(message)s", datefmt="%H:%M:%S"))
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
log = logging.getLogger("rich")


class StatusTracker:
    def __init__(self, title="Current Status"):
        self.title = title
        self.current_step = ""
        self.step_number = 0
        self.total_steps = 0
        self.errors = 0
        self.completed_steps = []
        self.live = None

    def __enter__(self):
        self.live = Live(self._create_status_panel(), refresh_per_second=4)
        self.live.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.live:
            self.live.__exit__(exc_type, exc_val, exc_tb)

    def set_total_steps(self, total):
        self.total_steps = total
        self._update_display()

    def start_step(self, step_name):
        self.step_number += 1
        self.current_step = step_name
        print(
            f"\n[bold blue]Starting Step {self.step_number}: {step_name}[/bold blue]")
        self._update_display()

    def complete_step(self, step_name=None):
        step_name = step_name or self.current_step
        timestamp = time.strftime('%H:%M:%S')
        self.completed_steps.append(f"✓ {timestamp} - {step_name} completed!")
        print(f"[bold green]✓ Completed: {step_name}[/bold green]")
        self._update_display()

    def add_error(self):
        self.errors += 1
        self._update_display()

    def _create_status_panel(self):
        status_text = f"""Current Step: {self.current_step}
Progress: {len(self.completed_steps)}/{self.total_steps} steps completed
Errors: {self.errors}
Time: {time.strftime('%H:%M:%S')}"""

        if self.completed_steps:
            status_text += "\n\nCompleted Steps:"
            # Show last 5 completed steps to avoid panel getting too large
            for step in self.completed_steps[-5:]:
                status_text += f"\n{step}"
            if len(self.completed_steps) > 5:
                status_text += f"\n... and {len(self.completed_steps) - 5} more"

        return Panel(status_text, title=self.title, border_style="blue")

    def _update_display(self):
        if self.live:
            self.live.update(self._create_status_panel())

# Example step functions


def do_this():
    print("  - Initializing data structures...")
    time.sleep(1)
    log.info("Data structures initialized")

    print("  - Loading configuration...")
    time.sleep(0.5)
    log.info("Configuration loaded successfully")

    print("  - Validating inputs...")
    time.sleep(0.3)
    log.info("Input validation complete")


def do_that():
    print("  - Connecting to database...")
    time.sleep(0.8)
    log.info("Database connection established")

    print("  - Fetching records...")
    time.sleep(1.2)
    log.info("Retrieved 150 records")

    print("  - Processing data...")
    time.sleep(0.7)
    log.info("Data processing complete")


def do_something_else():
    print("  - Generating reports...")
    time.sleep(1)
    log.info("Reports generated")

    print("  - Sending notifications...")
    time.sleep(0.5)
    log.info("Notifications sent to 5 users")

    print("  - Cleaning up temporary files...")
    time.sleep(0.3)
    log.info("Cleanup complete")


def do_final_step():
    print("  - Finalizing results...")
    time.sleep(0.8)
    log.info("Results finalized")

    print("  - Saving to disk...")
    time.sleep(0.4)
    log.info("Data saved successfully")

# Usage example


def main():
    with StatusTracker(title="Very nice status panel") as status:
        status.set_total_steps(4)

        # Step 1
        status.start_step("Initialize System")
        try:
            do_this()
            status.complete_step()
        except Exception as e:
            log.error(f"Error in step 1: {e}")
            status.add_error()

        # Step 2
        status.start_step("Process Data")
        try:
            do_that()
            status.complete_step()
        except Exception as e:
            log.error(f"Error in step 2: {e}")
            status.add_error()

        # Step 3
        status.start_step("Generate Output")
        try:
            do_something_else()
            status.complete_step()
        except Exception as e:
            log.error(f"Error in step 3: {e}")
            status.add_error()

        # Step 4
        status.start_step("Finalize")
        try:
            do_final_step()
            status.complete_step()
        except Exception as e:
            log.error(f"Error in step 4: {e}")
            status.add_error()

        print("\n[bold green]All steps completed![/bold green]")
        time.sleep(2)  # Let user see final status


if __name__ == "__main__":
    main()
