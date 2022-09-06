from rich.table import Table
from rich.console import Console


def show_result(statistics):
    table = Table(title="Insert benchmark")

    table.add_column("Storage", style="magenta")
    table.add_column("Mode", justify="right", style="cyan", no_wrap=True)
    table.add_column("Run Time \n (less is better)", justify="right", style="green")
    table.add_column("Speed per 1M insert \n (less is better)", justify="right", style="green")

    for row in statistics:
        if row["counter_insert"] != 0:
            insert_time = 1000000 * row["runtime_insert"] / row["counter_insert"]
            table.add_row(row["storage"], row["mode"], f'{row["runtime_insert"]:.3f}', f"{insert_time:.3f}")

    table2 = Table(title="Select benchmark")

    table2.add_column("Storage", style="magenta")
    table2.add_column("Run Time \n (less is better)", justify="right", style="green")
    table2.add_column("Speed per 1M select \n (less is better)", justify="right", style="green")

    for row in statistics:
        if row["counter_select"] != 0:
            select_time = 1000000 * row["runtime_select"] / row["counter_insert"]
            table2.add_row(row["storage"], f'{row["runtime_select"]:.3f}', f"{select_time:.3f}")

    console = Console()
    console.print(table)
    console.print(table2)
