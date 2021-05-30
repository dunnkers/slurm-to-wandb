# slurm-to-wandb
[![build status](https://github.com/dunnkers/slurm-to-wandb/actions/workflows/python-app.yml/badge.svg)](https://github.com/dunnkers/slurm-to-wandb/actions/workflows/python-app.yml) [![pypi badge](https://img.shields.io/pypi/v/slurm-to-wandb.svg?maxAge=3600)](https://pypi.org/project/slurm-to-wandb/)

 Monitor SLURM jobs using Weights and Biases (wandb) 📊

## Usage
On your cluster, login to wandb using the [cli](https://github.com/wandb/client), then run:

```shell
pip install slurm_to_wandb
slurm_to_wandb <job_ids>
```

... to upload all `sacct` information to wandb. To construct a DataFrame with the information yourself, run:

```python
from slurm_to_wandb import sacct_as_df

df = sacct_as_df(*<job_ids>)
df
```

Upload the information to wandb however you like 🙌🏻

## About
By [Jeroen Overschie](https://dunnkers.com/).