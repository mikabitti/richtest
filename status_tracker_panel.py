from rich.live import Live
from rich.panel import Panel
from rich import print
import time


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
