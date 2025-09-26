import numpy as np
import pandas as pd
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
        self.step_data = {}  # Store display data for current and completed steps
        self.step_results = {}  # Store actual returned data from steps
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

    def complete_step(self, step_name=None, result=None, **final_data):
        """Complete step with optional final data and actual result"""
        step_name = step_name or self.current_step
        timestamp = time.strftime('%H:%M:%S')

        # Store the actual result data separately
        if result is not None:
            self.step_results[step_name] = result

        # Add any final display data
        if final_data and step_name in self.step_data:
            self.step_data[step_name].update(final_data)

        # Create completion message with display data if available
        completion_msg = f"✓ {step_name} completed at {timestamp}"
        if step_name in self.step_data and self.step_data[step_name]:
            data_summary = self._format_step_data(self.step_data[step_name])
            if data_summary:
                completion_msg += f" ({data_summary})"

        self.completed_steps.append(completion_msg)
        print(f"[bold green]{completion_msg}[/bold green]")
        self._update_display()

        return result  # Return the result for chaining

    def get_step_result(self, step_name):
        """Get the actual result data from a completed step"""
        return self.step_results.get(step_name)

    def _format_step_data(self, data):
        """Format step data for display"""
        if not data:
            return ""

        formatted_parts = []
        for key, value in data.items():
            if key == "lines_processed":
                formatted_parts.append(f"{value:,} lines")
            elif key == "records_found":
                formatted_parts.append(f"{value:,} records")
            elif key == "output_file":
                formatted_parts.append(f"saved to {value}")
            elif key == "files_created":
                formatted_parts.append(f"{value} files created")
            elif key == "notifications_sent":
                formatted_parts.append(f"{value} notifications sent")
            elif key == "errors_found":
                formatted_parts.append(f"{value} errors found")
            elif key == "processing_time":
                formatted_parts.append(f"{value:.2f}s")
            elif key == "dataframe_shape":
                formatted_parts.append(f"df: {value[0]}×{value[1]}")
            elif key == "dataframe_memory":
                formatted_parts.append(f"{value:.1f}MB")
            elif key == "model_accuracy":
                formatted_parts.append(f"accuracy: {value:.2%}")
            else:
                # Generic formatting for other data types
                formatted_parts.append(f"{key}: {value}")

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

        return Panel(status_text, title="Processing Status", border_style="blue", height=20)

    def _update_display(self):
        if self.live:
            self.live.update(self._create_status_panel())


# Example step functions with real data passing


def load_data(status: StatusTracker):
    """Step 1: Load data and return DataFrame"""
    print("  - Reading CSV file...")
    time.sleep(1)

    # Simulate loading a DataFrame
    data = {
        'id': range(1, 1001),
        'value': np.random.randn(1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'timestamp': pd.date_range('2024-01-01', periods=1000, freq='H')
    }
    df = pd.DataFrame(data)

    # Update status with metadata about the DataFrame
    status.update_step_data(
        lines_processed=len(df),
        dataframe_shape=df.shape,
        dataframe_memory=df.memory_usage(deep=True).sum() / 1024**2  # MB
    )

    print(f"  - Loaded {len(df):,} records")
    log.info(f"DataFrame loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    return df  # Return the actual DataFrame


def process_data(status, df):
    """Step 2: Process the DataFrame and return processed data"""
    print("  - Cleaning data...")
    time.sleep(0.5)

    # Remove any missing values
    df_clean = df.dropna()
    status.update_step_data(records_after_cleaning=len(df_clean))

    print("  - Computing statistics...")
    time.sleep(0.8)

    # Add some computed columns
    df_clean['value_squared'] = df_clean['value'] ** 2
    df_clean['value_category'] = df_clean['value'].apply(
        lambda x: 'high' if x > 0.5 else 'low' if x < -0.5 else 'medium'
    )

    # Simulate some processing metrics
    high_values = (df_clean['value'] > 0.5).sum()
    status.update_step_data(
        high_value_records=high_values,
        categories_found=df_clean['category'].nunique()
    )

    print(f"  - Found {high_values} high-value records")
    log.info(f"Data processing complete: {len(df_clean)} clean records")

    return df_clean  # Return the processed DataFrame


def analyze_data(status, df):
    """Step 3: Analyze data and return results"""
    print("  - Running statistical analysis...")
    time.sleep(1.2)

    # Perform analysis
    analysis_results = {
        'mean_value': df['value'].mean(),
        'std_value': df['value'].std(),
        'category_counts': df['category'].value_counts().to_dict(),
        'correlation_matrix': df[['value', 'value_squared']].corr(),
        'summary_stats': df.describe()
    }

    # Update status with analysis metadata
    status.update_step_data(
        analyses_completed=5,
        mean_value=analysis_results['mean_value'],
        categories_analyzed=len(analysis_results['category_counts'])
    )

    print(
        f"  - Analysis complete, mean value: {analysis_results['mean_value']:.3f}")
    log.info("Statistical analysis completed")

    return analysis_results  # Return the analysis results


def save_results(status, df, analysis):
    """Step 4: Save data and analysis results"""
    print("  - Saving processed data...")
    time.sleep(0.6)

    # Save DataFrame (simulated)
    output_file = f"processed_data_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    # df.to_csv(output_file, index=False)  # Uncomment for real saving

    print("  - Saving analysis results...")
    time.sleep(0.4)

    # Save analysis (simulated)
    analysis_file = f"analysis_results_{time.strftime('%Y%m%d_%H%M%S')}.json"
    # import json
    # with open(analysis_file, 'w') as f:
    #     json.dump({k: v for k, v in analysis.items() if k != 'correlation_matrix'}, f, indent=2)

    status.update_step_data(
        data_file=output_file,
        analysis_file=analysis_file,
        records_saved=len(df)
    )

    print(f"  - Saved {len(df):,} records to {output_file}")
    log.info(f"Results saved: {output_file}, {analysis_file}")

    return {
        'data_file': output_file,
        'analysis_file': analysis_file,
        'records_saved': len(df)
    }

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

# Usage example - Passing real data between steps


def main():
    with StatusTracker() as status:
        status.set_total_steps(4)

        # Step 1: Load data
        status.start_step("Load Data")
        try:
            df = load_data(status)
            status.complete_step(result=df, processing_time=1.5)
        except Exception as e:
            log.error(f"Error in step 1: {e}")
            status.add_error()
            return

        # Step 2: Process the data from step 1
        status.start_step("Process Data")
        try:
            # Pass DataFrame from step 1
            processed_df = process_data(status, df)
            status.complete_step(result=processed_df, processing_time=1.3)
        except Exception as e:
            log.error(f"Error in step 2: {e}")
            status.add_error()
            return

        # Step 3: Analyze the processed data
        status.start_step("Analyze Data")
        try:
            analysis_results = analyze_data(
                status, processed_df)  # Pass processed DataFrame
            status.complete_step(result=analysis_results, processing_time=1.2)
        except Exception as e:
            log.error(f"Error in step 3: {e}")
            status.add_error()
            return

        # Step 4: Save both DataFrame and analysis results
        status.start_step("Save Results")
        try:
            save_info = save_results(
                status, processed_df, analysis_results)  # Pass both
            status.complete_step(result=save_info, processing_time=1.0)
        except Exception as e:
            log.error(f"Error in step 4: {e}")
            status.add_error()
            return

        print("\n[bold green]All steps completed![/bold green]")

        # You can also access stored results later
        final_df = status.get_step_result("Process Data")
        final_analysis = status.get_step_result("Analyze Data")
        print(
            f"Final DataFrame shape: {final_df.shape if final_df is not None else 'None'}")

        time.sleep(2)  # Let user see final status

# Alternative: Using a data context class for cleaner data passing


class DataContext:
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.analysis_results = None
        self.save_info = None


def main_with_context():
    """Alternative approach using a shared context object"""
    with StatusTracker() as status:
        status.set_total_steps(4)
        context = DataContext()

        # Step 1
        status.start_step("Load Data")
        try:
            context.raw_data = load_data(status)
            status.complete_step(result=context.raw_data, processing_time=1.5)
        except Exception as e:
            log.error(f"Error loading data: {e}")
            status.add_error()
            return

        # Step 2
        status.start_step("Process Data")
        try:
            context.processed_data = process_data(status, context.raw_data)
            status.complete_step(
                result=context.processed_data, processing_time=1.3)
        except Exception as e:
            log.error(f"Error processing data: {e}")
            status.add_error()
            return

        # Step 3
        status.start_step("Analyze Data")
        try:
            context.analysis_results = analyze_data(
                status, context.processed_data)
            status.complete_step(
                result=context.analysis_results, processing_time=1.2)
        except Exception as e:
            log.error(f"Error analyzing data: {e}")
            status.add_error()
            return

        # Step 4
        status.start_step("Save Results")
        try:
            context.save_info = save_results(
                status, context.processed_data, context.analysis_results)
            status.complete_step(result=context.save_info, processing_time=1.0)
        except Exception as e:
            log.error(f"Error saving results: {e}")
            status.add_error()
            return

        print("\n[bold green]All steps completed![/bold green]")
        print(f"Final DataFrame shape: {context.processed_data.shape}")
        time.sleep(2)

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
    # main()  # or main_with_context() for context approach
    # main_decorated()  # or main_decorated() for decorator approach
    main_with_context()
