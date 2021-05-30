 io  StringIO

 pytest
 slurm_to_wandb.sacct_to_df  (
    construct_df,
    parse_duration_string,
    parse_memory_string,
)



 test_parse_duration_str():
    duration = parse_duration_string(None)
     duration is None

    duration = parse_duration_string("01:00:00")
     duration == 3600

    duration = parse_duration_string("1-00:00:00")
     duration == 86400

    duration = parse_duration_string("0-00:00:00.234")
     duration == 0.000234

    duration = parse_duration_string("00:36.305")
     duration == 36.000305


 test_parse_memory_string():
    memory = parse_memory_string(None)
     memory is None

    memory = parse_memory_string("1000K")
     memory == 1

    memory = parse_memory_string("1G")
     memory == 1000


.fixture
 csv_input():
    file = open("tests/empty_sacct_job.csv")
    content = .read()
    string = StringIO(content)
     string


 test_empty_df_construction(csv_input):
    df = construct_df(csv_input)
     df not None
