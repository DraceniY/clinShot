import configparser
import argparse
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import complementTools
import allel

def main(clinvar_url, vcf_file_name, output_directory):
	"""
		Main function downloads vcf file, extract clinical variations and links between clinvar IDs (ID) and dbsnp IDs (RS) then write data in json format files.

		Args:
		vcf_file_name: <str> Name of vcf file in the website, this argument is optional.
		output_directory: <str> Path of the output directory, this argument is optional.

	"""
	# Check if output directory is provided
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

	# Parse ncbi clinvar page
	page = requests.get(clinvar_url)
	page_parser = BeautifulSoup(page.content, "html.parser")
	
	# Get all vcf names in the web page 
	vcf_files_list = [element["href"] for element in page_parser.find_all(href=True) if element["href"].endswith(".vcf.gz")]

	# Case file name provided in the config
	if vcf_file_name != None:
		# Verify if the file is in the ncbi clinvar ftp 
		if vcf_file_name not in vcf_files_list :
			print("This file " + vcf_file_name + " is not in " + clinvar_url + " website, please use vcf file available in the website.")
			exit()
	# Case file name is not provided, it downloads the first vcf file of the clinvar page
	else :
		vcf_file_name = vcf_files_list[0]
	
	# Download files in vcf, tbi and md5 formats
	print ("Start to download " + vcf_file_name + ", " + vcf_file_name + ".tbi, " + vcf_file_name + ".md5  files :")	
	vcf_file = complementTools.download_url(clinvar_url + vcf_file_name, output_directory)	
	index_vcf_file = complementTools.download_url(clinvar_url + vcf_file_name + ".tbi", output_directory)
	md5_vcf_file = complementTools.download_url(clinvar_url + vcf_file_name + ".md5", output_directory)

	# Parse vcf file and extract clinical data
	print("Currently parsing vcf file.")
	vcf_data = allel.vcf_to_dataframe(vcf_file, fields=['variants/*', 'calldata/*'])	
	nods_data, links_data = complementTools.extract_clinical_data(vcf_data)

	# Save data to json files  
	print("Nodes and Links json files are saved in " + output_directory)
	nods_data.to_json(output_directory + "/nodes.json", orient="records")
	links_data.to_json(output_directory + "/links.json", orient="records")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-url", help="Takes ftp clinvar url.", required=True)
	parser.add_argument("-vcf", help="Vcf file name in clinvar ftp file.")
	parser.add_argument("-output", help="Path for json data output.")
	args = parser.parse_args()

	main(args.url, args.vcf, args.output)
