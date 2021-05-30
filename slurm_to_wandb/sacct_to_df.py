import os
import re
import subprocess
from io import StringIO
from typing import List

import humanfriendly
import numpy as np
import pandas as pd
from pandas._typing import FilePathOrBuffer


def parse_duration_string(duration_str: str):
    if not duration_str:
        return duration_str

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


def parse_duration(series: pd.Series):
    return series.dropna().apply(parse_duration_string)


def parse_memory_string(memory_str: str):
    if not memory_str:
        return memory_str

    return humanfriendly.parse_size(memory_str) / 1e6


def parse_memory(series: pd.Series):
    return series.dropna().apply(parse_memory_string)


def construct_df(csv_input: FilePathOrBuffer):
    # read csv to data frame
    df = pd.read_csv(
        csv_input, sep=";", parse_dates=["Eligible", "End", "Start", "Submit"]
    )

    # parse durations
    df["Elapsed"] = parse_duration(df["Elapsed"])
    df["AveCPU"] = parse_duration(df["AveCPU"])
    df["MinCPU"] = parse_duration(df["MinCPU"])
    df["UserCPU"] = parse_duration(df["UserCPU"])
    df["CPUTime"] = parse_duration(df["CPUTime"])
    df["TotalCPU"] = parse_duration(df["TotalCPU"])
    df["Timelimit"] = parse_duration(df["Timelimit"])
    df["Suspended"] = parse_duration(df["Suspended"])

    # parse memory storage: from any amount to Megabytes
    df["AveCPUFreq"] = parse_memory(df["AveCPUFreq"])
    df["AveDiskRead"] = parse_memory(df["AveDiskRead"])
    df["AveDiskWrite"] = parse_memory(df["AveDiskWrite"])
    df["AveRSS"] = parse_memory(df["AveRSS"])
    df["AveVMSize"] = parse_memory(df["AveVMSize"])
    df["MaxDiskRead"] = parse_memory(df["MaxDiskRead"])
    df["MaxDiskWrite"] = parse_memory(df["MaxDiskWrite"])
    df["MaxRSS"] = parse_memory(df["MaxRSS"])
    df["MaxVMSize"] = parse_memory(df["MaxVMSize"])
    df["ReqMem"] = parse_memory(df["ReqMem"])

    # exit code
    parse_exit_code = lambda exit_code_str: int(exit_code_str.split(":")[1])
    df["ExitCode"] = df["ExitCode"].dropna().apply(parse_exit_code)

    return df


def sacct_as_csv(*job_ids: List[str]):
    helpformat = subprocess.run(["sacct", "--helpformat"], stdout=subprocess.PIPE)
    helpformat_str = helpformat.stdout.decode("utf-8")

    params = pd.read_csv(
        StringIO(helpformat_str), sep="\s.*", header=None, engine="python"
    )
    params = params.dropna(axis=1)
    params = params.values
    params = np.squeeze(params)
    params_str = ",".join(params)

    user = os.environ.get("USER")
    csv = subprocess.run(
        [
            "sacct",
            f"--format={params_str}",
            "--starttime",
            "2021-05-20",
            f"--jobs={','.join(job_ids)}",  # type: ignore
            "-u",
            f"{user}",
            "--parsable2",
            "--delimiter=;",
        ],
        stdout=subprocess.PIPE,
    )
    csv_str = csv.stdout.decode("utf-8")

    return csv_str


def sacct_as_df(*job_ids: List[str]):
    csv = sacct_as_csv(*job_ids)
    csv_input = StringIO(csv)
    df = construct_df(csv_input)

    return df
