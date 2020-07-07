cwlVersion: v1.0
class: Workflow

inputs:
    inputFile: File
    outputFileName: string
    mappingFile: File
 
outputs:
    outputFile:
        type: File
        outputSource: csv_to_json/outputFile

steps:
    csv_to_json:
        run: csv_to_json.cwl
        in:
            inputFile: inputFile
            outputFileName: outputFileName
            mappingFile: mappingFile
        out: [outputFile]