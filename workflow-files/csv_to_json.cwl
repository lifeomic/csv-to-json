cwlVersion: v1.0
class: CommandLineTool
hints:
    DockerRequirement:
        dockerPull: cluebbehusen/csv-to-json:1.0
    ResourceRequirement:
        coresMin: 1
        coresMax: 1
        ramMin: 4GB
        ramMax: 4GB

inputs:
    inputFile:
        type: File
        inputBinding:
            position: 1
            prefix: "-i"
    outputFileName:
        type: string
        inputBinding:
            position: 2
            prefix: "-o"
    mappingFile:
        type: File
        inputBinding:
            position: 3
            prefix: "-m"

outputs:
    outputFile:
        type: File
        outputBinding:
            glob: $(inputs.outputFileName)

baseCommand: ['python3', '/usr/src/app/csv_to_json/create_json_from_csv.py']