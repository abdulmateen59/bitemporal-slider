# Getting Started
The solution is containerized, use the following command to see the output, and to change the 
input refer to script `entrypoint.sh`
```sh
docker build . -t othoz && docker run --rm -it othoz
```
The CSV file is written inside the container, the volume can be mounted to persist the output file.

### Run locally
The following command can be used to run the package locally, output file will be written to data directory

```sh
python src/main.py --initial_start=2001-01-01 --end=2001-01-06 --system_time=2001-01-07 --sliding_steps=4 --sliding_delta=1
```
**Test Cases**
```sh
pytest tests
```

The same data set is used as in the example, the answer to the questions is also provided in the docstrings of the function.