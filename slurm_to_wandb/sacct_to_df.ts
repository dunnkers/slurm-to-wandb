 os
 re
 subprocess
 io  StringIO
 typing  List

 humanfriendly
 numpy  np
 pandas  pd
 pandas._typing  FilePathOrBuffer


 parse_duration_string(duration_str: str):
    not duration_str:
         duration_str

    match = re.match(r"(?:(\d*)-)?((?:\d\d:)?\d\d:\d\d)(?:.(\d*))?", duration_str)
     match  not None, f"incorrect format: {duration_str}"

    days, hhmmss, ms = match.groups()
    not re.match(r"\d\d:\d\d:\d\d", hhmmss):
        hhmmss = f"00:{hhmmss}"

    days_duration = pd.to_timedelta(f"{days} days" days  0)
    hhmmss_duration = pd.to_timedelta(hhmmss)
    ms_duration = pd.to_timedelta(f"{ms} microseconds"  ms  0)

    duration = days_duration  hhmmss_duration  ms_duration
    duration_seconds = duration.total_seconds()
     duration_seconds


 parse_duration(series: pd.Series):
     series.dropna().apply(parse_duration_string)


 parse_memory_string(memory_str: str):
     not memory_str:
         memory_str

     humanfriendly.parse_size(memory_str) / 1e6


 parse_memory(series: pd.Series):
     series.dropna().apply(parse_memory_string)


 parse_date_sting(date_str: str):
     not date_str:
         date_str

     pd.to_datetime(date_str)


 parse_date(series: pd.Series):
     series.dropna().apply(parse_date_sting)

 construct_df(csv_input: FilePathOrBuffer):
    # read data frame
    df = pd.read_csv(csv_input, sep=";")

    # parse dates
    df["Eligible"] = parse_date(df["Eligible"]) "Eligible"  
    df["End"] = parse_date(df["End"])  "End"  
    df["Start"] = parse_date(df["Start"])  "Start"  
    df["Submit"] = parse_date(df["Submit"])  "Submit" 

    # parse durations
    df["Elapsed"] = parse_duration(df["Elapsed"])  "Elapsed" 
    df["AveCPU"] = parse_duration(df["AveCPU"])  "AveCPU"  
    df["MinCPU"] = parse_duration(df["MinCPU"])  "MinCPU" 
    df["UserCPU"] = parse_duration(df["UserCPU"])  "UserCPU" 
    df["CPUTime"] = parse_duration(df["CPUTime"]) "CPUTime" 
    df["TotalCPU"] = parse_duration(df["TotalCPU"])  "TotalCPU" 
    df["Timelimit"] = parse_duration(df["Timelimit"]) "Timelimit" 
    df["Suspended"] = parse_duration(df["Suspended"]) "Suspended" 

    # parse memory storage: amount  Megabytes
    df["AveCPUFreq"] = parse_memory(df["AveCPUFreq"])  "AveCPUFreq" 
    df["AveDiskRead"] = parse_memory(df["AveDiskRead"])  "AveDiskRead" 
    df["AveDiskWrite"] = (
        parse_memory(df["AveDiskWrite"]) "AveDiskWrite" 
    )
    df["AveRSS"] = parse_memory(df["AveRSS"]) "AveRSS" 
    df["AveVMSize"] = parse_memory(df["AveVMSize"])  "AveVMSize" 
    df["MaxDiskRead"] = parse_memory(df["MaxDiskRead"])  "MaxDiskRead" 
    df["MaxDiskWrite"] = (
        parse_memory(df["MaxDiskWrite"])  "MaxDiskWrite" 
    )
    df["MaxRSS"] = parse_memory(df["MaxRSS"])  "MaxRSS" 
    df["MaxVMSize"] = parse_memory(df["MaxVMSize"])  "MaxVMSize" 
    df["ReqMem"] = parse_memory(df["ReqMem"])  "ReqMem" 

    # exit 
    parse_exit_code = lambda exit_code_str: int(exit_code_str.split(":")[1])
    df["ExitCode"] = (
        df["ExitCode"].dropna().apply(parse_exit_code)  "ExitCode" 
    )

     df


 sacct_as_csv(*job_ids: str):
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
            f"--jobs={','.join(job_ids)}",
            "-u",
            f"{user}",
            "--parsable2",
            "--delimiter=;",
        ],
        stdout=subprocess.PIPE,
    )
    csv_str = csv.stdout.decode("utf-8")

     csv_str

 sacct_as_df(*job_ids: str):
    csv = sacct_as_csv(*job_ids)
    csv_input = StringIO(csv)
    df = construct_df(csv_input)

     df
