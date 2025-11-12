# Protein design prototype

To run this:

- Make sure you have apptainer installed
- Make sure you have a cuda-enabled graphics card
- Clone proteindj somewhere (https://github.com/PapenfussLab/proteindj.git)
- Build the images in the `proteindj/apptainer` folder. There is a bash script for this

## setup

1. Clone this repository
2. Create a new conda/mamba env using the `environment.yml` in this directory, e.g. `mamba env create -f environment.yml`

## Running the web application
1. Activate the environment e.g. `mamba activate protein-safety`
2. Set important env variables
```bash
export DB_PATH=./pdbs.db
export OUTPUT_BASE_PATH=./proteindj_output
```  
3. Start the flask application for debugging using `flask --app pdbs_web run --debug`
  - For production, use an UWSGI solution
4. The application should be live on http://localhost:5000

## Running the worker (separate terminal)

1. Activate the environment e.g. `mamba activate protein-safety`
2. Set important env variables

```bash
export DB_PATH=./pdbs.db
export PROTEINDJ_PATH=./proteindj # adjust depending on where proteindj is
export PROTEINDJ_IMAGE_PATH=./proteindj/apptainer  # adjust depending on where proteindj is
export OUTPUT_BASE_PATH=./proteindj_output
```
3. Start the worker `python pdbs_worker/worker.py`


## important

Make sure the `DB_PATH` and `OTUPUT_BASE_PATH` variables point to the same location

