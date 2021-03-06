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

# Output
The tool creates two json files: ​ nodes.json (clinical variations)and ​ links.json ​ (links between clinvar IDs (ID) and dbsnp IDs (RS)).
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

# Dependencies
python=3.6.8
scikit-allel==1.3.2
argparse==1.4.0
pandas==0.25.0
wget==3.2
beautifulsoup4==4.9.3
requests==2.22.0
os-sys==2.1.4

# Copyright
YD - 2021
