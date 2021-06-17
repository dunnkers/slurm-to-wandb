import os
import re
import subprocess
from io import StringIO
from typing import List

import humanfriendly
import numpy as np
import pandas as pd
from pandas._typing import FilePathOrBuffer
from pandas.errors import ParserError


def parse_duration_string(duration_str: str):
    if not duration_str:
        return duration_str

    try:
        match = re.match(r"(?:(\d*)-)?((?:\d\d:)?\d\d:\d\d)(?:.(\d*))?", duration_str)
        assert match is not None, f"incorrect duration format: {duration_str}"

        days, hhmmss, ms = match.groups()
        if not re.match(r"\d\d:\d\d:\d\d", hhmmss):
            hhmmss = f"00:{hhmmss}"

        days_duration = pd.to_timedelta(f"{days} days" if days else 0)
        hhmmss_duration = pd.to_timedelta(hhmmss)
        ms_duration = pd.to_timedelta(f"{ms} microseconds" if ms else 0)

        duration = days_duration + hhmmss_duration + ms_duration
        duration_seconds = duration.total_seconds()
        return duration_seconds
    except Exception:
        return None


def parse_duration(series: pd.Series):
    return series.dropna().apply(parse_duration_string)


def parse_memory_string(memory_str: str):
    if not memory_str:
        return memory_str

    try:
        return humanfriendly.parse_size(memory_str) / 1e6
    except Exception:
        return None


def parse_memory(series: pd.Series):
    return series.dropna().apply(parse_memory_string)


def parse_date_sting(date_str: str):
    if not date_str:
        return date_str

    try:
        return pd.to_datetime(date_str)
    except Exception:
        return None


def parse_date(series: pd.Series):
    return series.dropna().apply(parse_date_sting)


def construct_df(csv_input: FilePathOrBuffer):
    # read csv to data frame
    df = pd.read_csv(csv_input, sep=";")

    # parse dates
    df["Eligible"] = parse_date(df["Eligible"]) if "Eligible" in df else None
    df["End"] = parse_date(df["End"]) if "End" in df else None
    df["Start"] = parse_date(df["Start"]) if "Start" in df else None
    df["Submit"] = parse_date(df["Submit"]) if "Submit" in df else None

    # parse durations
    df["Elapsed"] = parse_duration(df["Elapsed"]) if "Elapsed" in df else None
    df["AveCPU"] = parse_duration(df["AveCPU"]) if "AveCPU" in df else None
    df["MinCPU"] = parse_duration(df["MinCPU"]) if "MinCPU" in df else None
    df["UserCPU"] = parse_duration(df["UserCPU"]) if "UserCPU" in df else None
    df["CPUTime"] = parse_duration(df["CPUTime"]) if "CPUTime" in df else None
    df["TotalCPU"] = parse_duration(df["TotalCPU"]) if "TotalCPU" in df else None
    df["Timelimit"] = parse_duration(df["Timelimit"]) if "Timelimit" in df else None
    df["Suspended"] = parse_duration(df["Suspended"]) if "Suspended" in df else None

    # parse memory storage: from any amount to Megabytes
    df["AveCPUFreq"] = parse_memory(df["AveCPUFreq"]) if "AveCPUFreq" in df else None
    df["AveDiskRead"] = parse_memory(df["AveDiskRead"]) if "AveDiskRead" in df else None
    df["AveDiskWrite"] = (
        parse_memory(df["AveDiskWrite"]) if "AveDiskWrite" in df else None
    )
    df["AveRSS"] = parse_memory(df["AveRSS"]) if "AveRSS" in df else None
    df["AveVMSize"] = parse_memory(df["AveVMSize"]) if "AveVMSize" in df else None
    df["MaxDiskRead"] = parse_memory(df["MaxDiskRead"]) if "MaxDiskRead" in df else None
    df["MaxDiskWrite"] = (
        parse_memory(df["MaxDiskWrite"]) if "MaxDiskWrite" in df else None
    )
    df["MaxRSS"] = parse_memory(df["MaxRSS"]) if "MaxRSS" in df else None
    df["MaxVMSize"] = parse_memory(df["MaxVMSize"]) if "MaxVMSize" in df else None
    df["ReqMem"] = parse_memory(df["ReqMem"]) if "ReqMem" in df else None

    # exit code
    parse_exit_code = lambda exit_code_str: int(exit_code_str.split(":")[1])
    df["ExitCode"] = (
        df["ExitCode"].dropna().apply(parse_exit_code) if "ExitCode" in df else None
    )

    return df


def sacct_as_csv(*job_ids: str, **sacct_args):
    # obtain all possible sacct parameters using `sacct --helpformat`
    helpformat = subprocess.run(["sacct", "--helpformat"], stdout=subprocess.PIPE)
    helpformat_str = helpformat.stdout.decode("utf-8")

    # parse helpformat parameters
    params = pd.read_csv(
        StringIO(helpformat_str), sep="\s.*", header=None, engine="python"
    )
    params = params.dropna(axis=1)
    params = params.values
    params = np.squeeze(params)
    params_str = ",".join(params)

    # construct sacct command line arguments
    user = os.environ.get("USER")
    jobs = ",".join(job_ids)
    sacct_command = [
        "sacct",
        f"--format={params_str}",
        f"--jobs={jobs}",
        "-u",
        f"{user}",
        "--parsable2",
        "--delimiter=;",
    ]

    for parameter, value in sacct_args.items():
        sacct_command.append(f"--{parameter}")
        sacct_command.append(str(value))

    # run `sacct`
    csv = subprocess.run(sacct_command, stdout=subprocess.PIPE)
    csv_str = csv.stdout.decode("utf-8")

    return csv_str


def sacct_as_df(*job_ids: str):
    csv = sacct_as_csv(*job_ids)
    csv_input = StringIO(csv)
    df = construct_df(csv_input)

    return df
