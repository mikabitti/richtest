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
    def __init__(self):
        self.current_step = ""
        self.step_number = 0
        self.total_steps = 0
        self.errors = 0
        self.completed_steps = []
        self.step_data = {}  # Store data for current and completed steps
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
        self.step_data[step_name] = {}  # Initialize data storage for this step
        print(
            f"\n[bold blue]Starting Step {self.step_number}: {step_name}[/bold blue]")
        self._update_display()

    def update_step_data(self, **data):
        """Update data for the current step"""
        if self.current_step:
            self.step_data[self.current_step].update(data)
            self._update_display()

    def complete_step(self, step_name=None, **final_data):
        """Complete step with optional final data"""
        step_name = step_name or self.current_step
        timestamp = time.strftime('%H:%M:%S')

        # Add any final data
        if final_data and step_name in self.step_data:
            self.step_data[step_name].update(final_data)

        # Create completion message with data if available
        completion_msg = f"✓ {timestamp} - {step_name} completed!"
        if step_name in self.step_data and self.step_data[step_name]:
            data_summary = self._format_step_data(self.step_data[step_name])
            if data_summary:
                completion_msg += f" ({data_summary})"

        self.completed_steps.append(completion_msg)
        print(f"[bold green]{completion_msg}[/bold green]")
        self._update_display()

    def _format_step_data(self, data):
        """Format step data for display"""
        if not data:
            return ""

        formatted_parts = []
        for key, value in data.items():
            if key == "lines_processed":
                formatted_parts.append(f"[green]{value:,}[/green] lines")
            elif key == "records_found":
                formatted_parts.append(f"[green]{value:,}[/green] records")
            elif key == "output_file":
                formatted_parts.append(f"saved to [green]{value}[/green]")
            elif key == "files_created":
                formatted_parts.append(f"[green]{value}[/green] files created")
            elif key == "notifications_sent":
                formatted_parts.append(
                    f"[green]{value}[/green] notifications sent")
            elif key == "errors_found":
                formatted_parts.append(f"[red]{value}[/red] errors found")
            elif key == "processing_time":
                formatted_parts.append(f"[green]{value:.2f}[/green]s")
            else:
                # Generic formatting for other data types
                formatted_parts.append(f"{key}: [green]{value}[/green]")

        return ", ".join(formatted_parts)

    def add_error(self):
        self.errors += 1
        self._update_display()

    def _create_status_panel(self):
        status_text = f"""Current Step: {self.current_step}
Progress: {len(self.completed_steps)}/{self.total_steps} steps completed
Errors: {self.errors}
Time: {time.strftime('%H:%M:%S')}"""

        # Add current step data if available
        if self.current_step and self.current_step in self.step_data:
            current_data = self._format_step_data(
                self.step_data[self.current_step])
            if current_data:
                status_text += f"\nCurrent Data: {current_data}"

        if self.completed_steps:
            status_text += "\n\nCompleted Steps:"
            # Show last 5 completed steps to avoid panel getting too large
            for step in self.completed_steps[-5:]:
                status_text += f"\n{step}"
            if len(self.completed_steps) > 5:
                status_text += f"\n... and {len(self.completed_steps) - 5} more"

        return Panel(status_text, title="Processing Status", border_style="blue")

    def _update_display(self):
        if self.live:
            self.live.update(self._create_status_panel())

# Example step functions with data tracking


def do_this(status):
    print("  - Initializing data structures...")
    time.sleep(1)
    log.info("Data structures initialized")

    print("  - Loading configuration...")
    time.sleep(0.5)
    log.info("Configuration loaded successfully")

    print("  - Validating inputs...")
    time.sleep(0.3)
    config_items = 42
    status.update_step_data(config_items=config_items)
    log.info(f"Input validation complete - {config_items} items validated")

    return {"config_loaded": True, "validation_passed": True}


def do_that(status):
    print("  - Connecting to database...")
    time.sleep(0.8)
    log.info("Database connection established")

    print("  - Fetching records...")
    time.sleep(1.2)
    records_found = 1547
    status.update_step_data(records_found=records_found)
    log.info(f"Retrieved {records_found:,} records")

    print("  - Processing data...")
    lines_processed = 0
    for i in range(10):  # Simulate processing
        lines_processed += 150 + (i * 10)
        status.update_step_data(lines_processed=lines_processed)
        time.sleep(0.07)

    log.info(f"Data processing complete - {lines_processed:,} lines processed")
    return {"records": records_found, "lines": lines_processed}


def do_something_else(status):
    print("  - Generating reports...")
    time.sleep(1)
    files_created = 3
    status.update_step_data(files_created=files_created)
    log.info(f"Reports generated - {files_created} files created")

    print("  - Sending notifications...")
    time.sleep(0.5)
    notifications_sent = 5
    status.update_step_data(notifications_sent=notifications_sent)
    log.info(f"Notifications sent to {notifications_sent} users")

    print("  - Cleaning up temporary files...")
    time.sleep(0.3)
    log.info("Cleanup complete")

    return {"reports": files_created, "notifications": notifications_sent}


def do_final_step(status):
    print("  - Finalizing results...")
    time.sleep(0.8)
    log.info("Results finalized")

    print("  - Saving to disk...")
    time.sleep(0.4)
    output_file = "results_2025_09_26.json"
    status.update_step_data(output_file=output_file)
    log.info(f"Data saved successfully to {output_file}")

    return {"output_file": output_file, "status": "completed"}

# Alternative: Decorator approach for automatic step tracking


def step(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if hasattr(wrapper, '_status_tracker'):
                wrapper._status_tracker.start_step(name)
                try:
                    result = func(*args, **kwargs)
                    wrapper._status_tracker.complete_step()
                    return result
                except Exception as e:
                    log.error(f"Error in {name}: {e}")
                    wrapper._status_tracker.add_error()
                    raise
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

# Decorated step functions (alternative approach)


@step("Initialize System")
def do_this_decorated():
    print("  - Initializing data structures...")
    time.sleep(1)
    log.info("Data structures initialized")


@step("Process Data")
def do_that_decorated():
    print("  - Connecting to database...")
    time.sleep(0.8)
    log.info("Database connection established")

# Usage example - Manual approach with data tracking


def main():
    with StatusTracker() as status:
        status.set_total_steps(4)

        # Step 1
        status.start_step("Initialize System")
        try:
            result = do_this(status)
            status.complete_step(processing_time=1.8)
        except Exception as e:
            log.error(f"Error in step 1: {e}")
            status.add_error()

        # Step 2
        status.start_step("Process Data")
        try:
            result = do_that(status)
            # You can pass final data to complete_step
            status.complete_step(processing_time=2.1)
        except Exception as e:
            log.error(f"Error in step 2: {e}")
            status.add_error()

        # Step 3
        status.start_step("Generate Output")
        try:
            result = do_something_else(status)
            status.complete_step(processing_time=1.8)
        except Exception as e:
            log.error(f"Error in step 3: {e}")
            status.add_error()

        # Step 4
        status.start_step("Finalize")
        try:
            result = do_final_step(status)
            status.complete_step(processing_time=1.2)
        except Exception as e:
            log.error(f"Error in step 4: {e}")
            status.add_error()

        print("\n[bold green]All steps completed![/bold green]")
        time.sleep(2)  # Let user see final status

# Alternative usage with decorators


def main_decorated():
    with StatusTracker() as status:
        status.set_total_steps(2)

        # Attach status tracker to functions
        do_this_decorated._status_tracker = status
        do_that_decorated._status_tracker = status

        # Now just call the functions - they'll auto-track
        do_this_decorated()
        do_that_decorated()

        print("\n[bold green]All steps completed![/bold green]")
        time.sleep(2)


if __name__ == "__main__":
    main()  # or main_decorated() for decorator approach
    # main_decorated()
