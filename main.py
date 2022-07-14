import argparse
import os
from pathlib import Path
from typing import List

import allel
import requests
import structlog
from bs4 import BeautifulSoup

import complementTools

logging = structlog.getLogger()


def main(clinvar_url: str, vcf_file_name: str, output_directory: Path):
    """
    Main function downloads vcf file, extract clinical variations and links between clinvar IDs (ID) and dbsnp IDs (RS) then write data in json format files.

    Args:
    vcf_file_name: <str> Name of vcf file in the website, this argument is optional.
    output_directory: <str> Path of the output directory, this argument is optional.

    """
    # Check if output directory is provided
    if output_directory != None and not output_directory.exists():
        output_directory.mkdir(parents=True, exist_ok=True)
    else:
        output_directory = Path(os.getcwd()) / "output"
        output_directory.mkdir(parents=True, exist_ok=True)

    # Parse ncbi clinvar page
    page = requests.get(clinvar_url)
    page_parser = BeautifulSoup(page.content, "html.parser")

    # Get all vcf names in the web page
    vcf_files_list = [
        element["href"]
        for element in page_parser.find_all(href=True)
        if element["href"].endswith(".vcf.gz")
    ]

    # Case file name provided in the config
    if vcf_file_name != None:
        # Verify if the file is in the ncbi clinvar ftp
        if vcf_file_name not in vcf_files_list:
            logging.error(
                f"This file {vcf_file_name} is not in {clinvar_url} website, please use vcf file available in the website."
            )
            exit()
    # Case file name is not provided, it downloads the first vcf file of the clinvar page
    else:
        vcf_file_name = vcf_files_list[0]

    # Download files in vcf, tbi and md5 formats
    logging.info(
        f"Start to download {vcf_file_name} {vcf_file_name}.tbi, {vcf_file_name}.md5  files :"
    )
    # Force conversion to string because wget.py accept string format and not Path in line 529
    vcf_file = complementTools.download_url(
        f"{clinvar_url}{vcf_file_name}", str(output_directory)
    )
    _ = complementTools.download_url(
        f"{clinvar_url}{vcf_file_name}.tbi", str(output_directory)
    )
    _ = complementTools.download_url(
        f"{clinvar_url}{vcf_file_name}.md5", str(output_directory)
    )

    # Parse vcf file and extract clinical data
    logging.info("Currently parsing vcf file.")
    vcf_data = allel.vcf_to_dataframe(vcf_file, fields=["variants/*", "calldata/*"])
    nods_data, links_data = complementTools.extract_clinical_data(vcf_data)

    # Save data to json files
    logging.info(f"Nodes and Links json files are saved in {output_directory}")
    nods_data.to_json(output_directory / "nodes.json", orient="records")
    links_data.to_json(output_directory / "links.json", orient="records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-url",
        help="URL clinvar eg:https://ftp.ncbi.nlm.nih.gov/.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-vcf", help="VCF file name for clinvar ftp file.", type=str.lower
    )
    parser.add_argument("-output", help="Path for files json output.", type=Path)
    args = parser.parse_args()

    main(args.url, args.vcf, args.output)
