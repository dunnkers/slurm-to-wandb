from io import StringIO

import pytest
from slurm_to_wandb.sacct_to_df import (construct_df, parse_duration_string,
                                        parse_memory_string)


def test_parse_duration_str():
    duration = parse_duration_string(None)
    assert duration is None

    duration = parse_duration_string("01:00:00")
    assert duration == 3600

    duration = parse_duration_string("1-00:00:00")
    assert duration == 86400

    duration = parse_duration_string("0-00:00:00.234")
    assert duration == 0.000234

    duration = parse_duration_string("00:36.305")
    assert duration == 36.000305


def test_parse_memory_string():
    memory = parse_memory_string(None)
    assert memory is None

    memory = parse_memory_string("1000K")
    assert memory == 1

    memory = parse_memory_string("1G")
    assert memory == 1000


def get_csv_as_string(filepath):
    file = open(filepath)
    content = file.read()
    string = StringIO(content)

    return string


@pytest.fixture
def empty_job():
    return get_csv_as_string("tests/empty_job.csv")


def test_empty_job_df_construction(empty_job):
    df = construct_df(empty_job)
    assert df is not None


@pytest.fixture
def running_job():
    return get_csv_as_string("tests/running_job.csv")


def test_running_job_df_construction(running_job):
    df = construct_df(running_job)
    assert df is not None
