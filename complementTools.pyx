import pandas as pd
import wget

def download_url(url, output_directory):
	"""
		This function downloads url and saves the file in the provided output directory.

		Args:
		url: <str> The url link of the ncbi website.
		output_directory: <str> Path of output directory.

		Returns:
		vcf_file: <str> Path of the downloaded file.

	"""
	vcf_file = wget.download(url, out=output_directory)	

	return vcf_file

def extract_clinical_data(vcf_data):
	"""
		This function extracts data from dataframe of clinical variations and returns two dataframes with specific fields.

		Args:
		vcf_data: <dataframe> A dataframe containing data of clinical variations in vcf file format.

		Returns:
		nods_data: <dataframe> A dataframe containing informations of variant.
		links_data: <dataframe> A dataframe containing position start and end of variant.

	"""
	
	# Create dataframes for nods and links data
	nods_data = pd.DataFrame(columns=["CHROM","POS","ID","REF","ALT","AF_ESP","AF_EXAC","AF_TGP","ALLELEID"])
	links_data = pd.DataFrame(columns=["_from","_to"])

	# Extract clinical variations
	nods_data["CHROM"] = vcf_data["CHROM"]
	nods_data["POS"] = vcf_data["POS"]	
	nods_data["ID"] = vcf_data["ID"]
	nods_data["REF"] = vcf_data["REF"]
	nods_data["ALT"] = vcf_data["ALT_1"]
	nods_data["AF_ESP"] = vcf_data["AF_ESP"]
	nods_data["AF_EXAC"] = vcf_data["AF_EXAC"]
	nods_data["AF_TGP"] = vcf_data["AF_TGP"]
	nods_data["ALLELEID"] = vcf_data["ALLELEID"]

	# Extract links between clinvar IDs (ID) and dbsnp IDs (RS)
	links_data["_from"] = vcf_data["ID"]
	links_data["_to"] = vcf_data["RS"]

	return nods_data, links_data		
