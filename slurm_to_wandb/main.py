import sys

import wandb

from .sacct_to_df import sacct_as_df


def main():
    # job ids
    job_ids = sys.argv[1:]

    # get job information from `sacct`
    print("constructing pandas dataframe...")
    df = sacct_as_df(*job_ids)
    print("dataframe constructed ✓")

    # upload to wandb
    for index, result in df.iterrows():
        wandb.init(
            project="peregrine",
            config=result.to_dict(),
            id=result["JobID"],
            job_type=result["JobName"],
            name=result["JobID"],
            tags=[result["State"]],
        )
        wandb.finish(exit_code=result["ExitCode"])


if __name__ == "__main__":
    main()
