# clinShot

`clinShot` is a tool that provides latest [Clinvar](https://www.ncbi.nlm.nih.gov/clinvar/) database in json format for Homo sapiens (human) genome assembly [Grch38](https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/) version. 
`clinShot` downloads and analyzes a VCF file in your choice (in case you want to precise the file) or clinvar VCF file from [ncbi database](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/). Then, it extracts clinical variations, links them with clinvar IDs (ID) and dbsnp IDs (RS).

# Installation

`clinShot` uses several python packages. `Docker` allows to manage the environment and dependencies. Please see the [instructions](https://docs.docker.com/engine/install/ubuntu/) to install `Docker`.

# Usage 

A brief guide of how to use `clinShot` :

The setup file `setup.py` cythonizes `complementTools.pyx` packages by compiling them in C/C++, and use the compiled tools to maximize the run. The main script has three parameters as following :

```
USAGE: main.py [OPTIONS]
OPTIONS:
  -url URL                  URL to NCBI Clinvar page. This should not return
                            direct vcf file. [Required] 
                            
  -vcf VCF                  Name of the vcf file available in the NCBI Clinvar page. [Optional]
  
  -output OUTPUT            Path to desired output folder. Defaults to the
                            same place as the specified output folder. [Optional]

```

## Run from the container Docker : 
To facilitate environmental management, you can easily run and get the results from `Docker` container in the `output` folder using those command lines:

```
# Build Docker image
docker build --tag clinshot .
# Run the pipeline using one parameter (-url) and get the output results in output folder
docker container run -v $PWD/output:/output clinshot:latest -url https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/ -vcf homo_sapiens
```

## Run locally :
You need to install [anaconda](https://www.anaconda.com/) to install packages. If you don't have anaconda please see [instructions](https://docs.anaconda.com/anaconda/install/) to install it, then run locally:

```
conda env create -f requirements.yml
conda activate clinshot
python main.py -url https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/ -vcf homo_sapiens -output_directory clinical_output
```

# Output

The tool creates two json files: nodes.json (clinical variations) and links.json (links between clinvar IDs (ID) and dbsnp IDs (RS)).

### nodes.json :
```
[{
"CHROM": "1",
"POS": 1014042,
"ID": "475283",
"REF": "G",
"ALT": "A",
"AF_ESP": 0.00546,
"AF_EXAC": 0.00165,
"AF_TGP": 0.00619,
"ALLELEID": 446939
}]
```
### links.json
```
[{
"_from": "475283",
"_to": "143888043"
}]
and links.json:
[{
"_from": "475283",
"_to": "143888043"
}]
```

# Copyright
Yasmine Draceni - 2021
