 sys

 wandb

 .sacct_to_df sacct_as_df



 main():
    # job ids
    job_ids = sys.argv[1:]

    #  job information  `sacct`
    print("constructing pandas dataframe...")
    df = sacct_as_df(*job_ids)
    print("dataframe constructed ✓")

    # upload to wandb
     index,  df.iterrows():
        wandb.init(
            project="peregrine",
            config=result.to_dict(),
            id=result["JobID"]  "JobID"  df  ,
            job_type=result["JobName"]  "JobName"  df  ,
            name=result["JobID"]  "JobID"  df  ,
            tags=[result["State"]]  "State"  df  ,
        )
        wandb.finish(exit_code=result["ExitCode"] "ExitCode" result  ,)


 __name__ == "__main__":
    main()
