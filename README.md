# clinShot

`clinShot` is a tool that provides latest [Clinvar](https://www.ncbi.nlm.nih.gov/clinvar/) database in json format for [Grch38](https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/) version. 
`clinShot` downloads and analyzes a VCF file in your choice (in case you want to precise the file) or clinvar VCF file from [ncbi database](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/). Then, it extracts clinical variations and links between clinvar IDs (ID) and dbsnp IDs (RS) and save clinical data in json format files.

# Installation
While `clinShot` use several python package, you need to use dockerfile to install all packages and dependencies before to lunch the pipeline.

# Usage 
A brief guide of how to use `clinShot` 
In setup file, setuptools package allows `complementTools.pyx` to pass to compiled extension C/C++ file. The following command line to run the setup script :

```
python setup.py build_ext --inplace
```
Once done, run the main script following the manual :

```
USAGE: main.py [OPTIONS]
OPTIONS:
  -url URL                  URL to NCBI Clinvar page. This should not return
                            direct vcf file. [required] 
                            
  -vcf VCF                  Name of the vcf file available in the NCBI Clinvar page.
  
  -output OUTPUT            Path to desired output folder. Defaults to the
                            same place as the specified output folder.

```

# Copyright
YD - 2021
