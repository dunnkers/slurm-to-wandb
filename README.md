# slurm-to-wandb
[![build status](https://github.com/dunnkers/slurm-to-wandb/actions/workflows/python-app.yml/badge.svg)](https://github.com/dunnkers/slurm-to-wandb/actions/workflows/python-app.yml) [![pypi badge](https://img.shields.io/pypi/v/slurm-to-wandb.svg?maxAge=3600)](https://pypi.org/project/slurm-to-wandb/)

 Monitor SLURM jobs using Weights and Biases (wandb) 📊

## Usage
On your cluster, login to wandb using the [cli](https://github.com/wandb/client), then run:

```shell
pip install slurm-to-wandb
slurm_to_wandb <job_ids>
```

... to upload all `sacct` information to wandb. Currently, uploads to a project called "peregrine" - support for configuring this is planned #4. `<job_ids>` can be multiple space-separated job ids. In the case multiple job id's match, all matched job ids are uploaded (useful, for example, when using job arrays).

To construct a DataFrame with the information yourself, use the function `slurm_to_wandb.sacct_as_df(*job_ids, **sacct_args)`. `sacct_args` can be any additional args to pass to `sacct`. Run it on the cluster:

```python
from slurm_to_wandb import sacct_as_df

df = sacct_as_df("job_id_123", "another_job_id", starttime="2021-05-20")
df
```

You can now upload the information to wandb however you like 🙌🏻

## About
By [Jeroen Overschie](https://dunnkers.com/).