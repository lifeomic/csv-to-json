# CSV to JSON Mapping Tool

The CSV to JSON Mapping Tool is a script that allow one to transform each row (or column) in a CSV file into a JSON object in a JSON lines file based on a given mapping file. The mapping file is a JSON file that specifies how the JSON objects that are outputted should be structured. The mapping file can can also contain instructions to perform transforms on the data from the CSV file before it is outputted. See [transforms](./accepted_transformations.md) for more information about valid transforms.

## Usage

```bash
python3 csv-to-json/create_json_from_csv.py --help
```

## Testing

```bash
make test
```

## Linting

```bash
make lint
```

## Docker Container

This repo already contains a valid Dockerfile and a .dockerignore file. To create a docker container containing only the scripts necessary to run the program, run the following command.

```bash
docker build -t <tag name> .
```
