"""
    用于显示年月日时间进度
"""

import time
from datetime import datetime
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
)
from rich.live import Live


def get_year_progress():
    """
    获取年进度信息
    :return: year_progress, total_days_in_year
    """
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    end_of_year = datetime(now.year + 1, 1, 1)
    year_progress = (now - start_of_year).days + 1
    total_days_in_year = (end_of_year - start_of_year).days
    return year_progress, total_days_in_year


def get_month_progress():
    """
    获取月进度信息
    :return: month_progress, total_days_in_month
    """
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    end_of_month = now.month % 12 + 1
    next_month_year = now.year if end_of_month != 1 else now.year + 1
    start_of_next_month = datetime(next_month_year, end_of_month, 1)
    month_progress = (now - start_of_month).days + 1
    total_days_in_month = (start_of_next_month - start_of_month).days
    return month_progress, total_days_in_month


def get_day_progress():
    """
    获取日进度信息
    :return: day_progress, total_seconds_in_day
    """
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_progress = (now - start_of_day).seconds
    total_seconds_in_day = 86400
    return day_progress, total_seconds_in_day


progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.0f}%",
    TextColumn("{task.completed}/{task.total}"),
    expand=True
)

with Live(progress, refresh_per_second=10):
    year_task = progress.add_task("[bold red]Year Progress: ", total=get_year_progress()[1])
    month_task = progress.add_task("[bold yellow]Month Progress: ", total=get_month_progress()[1])
    day_task = progress.add_task("[bold blue]Day Progress: ", total=get_day_progress()[1])

    try:
        while True:
            progress.update(year_task, completed=get_year_progress()[0])
            progress.update(month_task, completed=get_month_progress()[0])
            progress.update(day_task, completed=get_day_progress()[0])

            time.sleep(1)
    except KeyboardInterrupt:
        pass
