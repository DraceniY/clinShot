import cyvcf2
import json
import configparser
import argparse
import requests
from bs4 import BeautifulSoup
import wget
import os
import pandas as pd


def extract_clinical_data(vcf):
	"""
		This function extract data from vcf file and returns two dataframes with specific fields.

		Args:
		vcf: <str> The ath of vcf file.

		Returns:
		nods_data: <dataframe> A dataframe containing informations of variant.
		links_data: <dataframe> A dataframe containing position start and end of variant.

	"""
	nods_data = pd.DataFrame(columns=["CHROM","POS","ID","REF","ALT","AF_ESP","AF_EXAC","AF_TGP","ALLELEID"])
	links_data = pd.DataFrame(columns=["_from","_to"])
	nods_dict = {}
	links_dict = {}

	for variant in vcf:
		# Extract clinical variations
		nods_dict["CHROM"] = variant.CHROM
		nods_dict["POS"] = variant.POS	
		nods_dict["ID"] = variant.ID
		nods_dict["REF"] = variant.REF
		nods_dict["ALT"] = "".join(variant.ALT)
		nods_dict["AF_ESP"] = variant.INFO.get("AF_ESP")
		nods_dict["AF_EXAC"] = variant.INFO.get("AF_EXAC")
		nods_dict["AF_TGP"] = variant.INFO.get("AF_TGP")
		nods_dict["ALLELEID"] = variant.INFO.get("ALLELEID")

		# Extract links between clinvar IDs (ID) and dbsnp IDs (RS)
		links_dict["_from"] = variant.ID
		links_dict["_to"] = variant.INFO.get("RS")

		nods_data = nods_data.append(nods_dict, ignore_index=True)
		links_data = links_data.append(links_dict, ignore_index=True)

	return nods_data, links_data			

def main(clinvar_url, vcf_file_name, output_directory, number_threads):
	"""
		Main function downloads vcf file, extract clinical variations and links between clinvar IDs (ID) and dbsnp IDs (RS) then write data in json format files.

		Args:
		vcf_file_name: <str> Name of vcf file in the website, this argument is optional.
		output_directory: <str> Path of the output directory, this argument is optional.

	"""
	print(output_directory)
	if(output_directory != None):
		if (os.path.exists(output_directory)):	
		# Remove / at the end of output directory in case if the user put it in the path
			if output_directory.endswith("/"):
				output_directory = output_directory[:-1]
		else:
			os.mkdir(output_directory)
	else:	
		os.system("mkdir output")
		output_directory = os.getcwd() + "/output"

	# Parse ncbi clinvar url
	page = requests.get(clinvar_url)
	page_parser = BeautifulSoup(page.content, "html.parser")
	
	# Case file name provided in the config
	vcf_files_list =[element["href"] for element in page_parser.find_all(href=True) if element["href"].endswith(".vcf.gz")]
	
	if vcf_file_name != None:
		# Verify if the file is in the ncbi clinvar ftp 
		if vcf_file_name not in vcf_files_list :
			print("This file " + vcf_file_name + " is not in https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/ website, please use vcf file available in the website")
			exit()
	else :
		vcf_file_name = vcf_files_list[0]
		
	vcf_file = wget.download(clinvar_url + vcf_file_name, out=output_directory)	
	index_vcf_file = wget.download(clinvar_url + vcf_file_name + ".tbi", out=output_directory)
	md5_vcf_file = wget.download(clinvar_url + vcf_file_name + ".md5", out=output_directory)

	# index vcf file
	os.system("tabix -p vcf " + vcf_file)

	# parse vcf file and extract clinical data
	vcf_parsed = cyvcf2.VCF(vcf_file)
	nods_data, links_data = extract_clinical_data(vcf_parsed)

	# Save data to json files  
	nods_data.to_json(output_directory + "/nodes.json", orient="records")
	links_data.to_json(output_directory + "/links.json", orient="records")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-url", help="Takes ftp clinvar url.", required=True)
	parser.add_argument("-vcf", help="Vcf file name in clinvar ftp file.")
	parser.add_argument("-output", help="Path for json data output")
	parser.add_argument("-n", help="Number of threads", default=1, type=int)
	args = parser.parse_args()

	main(args.url, args.vcf, args.output, args.n)
