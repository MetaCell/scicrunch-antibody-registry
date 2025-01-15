# Generated by Django 4.2.11 on 2025-01-03 11:11

from django.db import migrations
from django.core.files import File
import os

common_file_path_for_partners_image_data = "api/migrations/data/partners"

partners = [
    {"name": "thermofisher", "url": "https://www.thermofisher.com/", "image": f"{common_file_path_for_partners_image_data}/thermofisher.jpg"},
    {"name": "proteintech", "url": "https://www.ptglab.com/", "image": f"{common_file_path_for_partners_image_data}/proteintech.jpg"},
    {"name": "biocell", "url": "https://bxcell.com/", "image": f"{common_file_path_for_partners_image_data}/biocell.jpg"},
    {"name": "chromotek", "url": "http://www.chromotek.com/home-of-alpaca-antibodies/", "image": f"{common_file_path_for_partners_image_data}/chromotek.jpg"},
    {"name": "jesselllab", "url": "https://jesselllab.com/", "image": f"{common_file_path_for_partners_image_data}/jesselllab.jpg"},
    {"name": "encorbio", "url": "https://encorbio.com/", "image": f"{common_file_path_for_partners_image_data}/encorbio.jpg"},
    {"name": "biolegend", "url": "https://www.biolegend.com/", "image": f"{common_file_path_for_partners_image_data}/biolegend.jpg"},
    {"name": "leinco", "url": "https://www.leinco.com/", "image": f"{common_file_path_for_partners_image_data}/leinco.jpg"},
    {"name": "jacksonimmuno", "url": "https://www.jacksonimmuno.com/", "image": f"{common_file_path_for_partners_image_data}/jacksonimmuno.jpg"},
    {"name": "dshb", "url": "http://dshb.biology.uiowa.edu/", "image": f"{common_file_path_for_partners_image_data}/dshb.jpg"},
    {"name": "immunostar", "url": "http://immunostar.com/", "image": f"{common_file_path_for_partners_image_data}/immunostar.jpg"},
    {"name": "neuromab", "url": "http://neuromab.ucdavis.edu/", "image": f"{common_file_path_for_partners_image_data}/neuromab.jpg"},
    {"name": "sysy", "url": "https://www.sysy.com/", "image": f"{common_file_path_for_partners_image_data}/sysy.jpg"},
    {"name": "atlasantibodies", "url": "https://atlasantibodies.com/", "image": f"{common_file_path_for_partners_image_data}/atlasantibodies.jpg"},
    {"name": "frontier", "url": "https://www.frontier-institute.com/wp/antibodies/?lang=en", "image": f"{common_file_path_for_partners_image_data}/frontier.jpg"},
    {"name": "aeonianbiotech", "url": "https://aeonianbiotech.com/", "image": f"{common_file_path_for_partners_image_data}/aeonianbiotech.jpg"},
    {"name": "bdbiosciences", "url": "http://www.bdbiosciences.com/us/home", "image": f"{common_file_path_for_partners_image_data}/bdbiosciences.jpg"},
    {"name": "miltenyibiotec", "url": "https://www.miltenyibiotec.com/US-en/", "image": f"{common_file_path_for_partners_image_data}/miltenyibiotec.jpg"},
    {"name": "revmab", "url": "https://www.revmab.com/", "image": f"{common_file_path_for_partners_image_data}/revmab.jpg"},
    {"name": "southernbiotech", "url": "https://www.southernbiotech.com/", "image": f"{common_file_path_for_partners_image_data}/southernbiotech.jpg"},
    {"name": "wagner", "url": "http://gwagner.med.harvard.edu/", "image": f"{common_file_path_for_partners_image_data}/wagner.jpg"},
    {"name": "zebrafish", "url": "https://zebrafish.org/home/guide.php", "image": f"{common_file_path_for_partners_image_data}/zebrafish.jpg"},
    {"name": "genetex", "url": "https://www.genetex.com/", "image": f"{common_file_path_for_partners_image_data}/genetex.jpg"},
    {"name": "licor", "url": "https://www.licor.com/bio", "image": f"{common_file_path_for_partners_image_data}/LICORbio.png"},
    {"name": "hytest", "url": "https://www.hytest.fi/home", "image": f"{common_file_path_for_partners_image_data}/hytest.jpg" },
    {"name": "Ansh Labs", "url": "https://www.anshlabs.com/", "image": f"{common_file_path_for_partners_image_data}/anshlabs.png"},
    {"name": "Oasis Biofarm", "url": "https://www.oasisbiofarm.net", "image": f"{common_file_path_for_partners_image_data}/oasis.png"},
    {"name": "Nittobo Medical", "url": "https://www.nittobo.co.jp/", "image": f"{common_file_path_for_partners_image_data}/Nittobo.png"},
    {"name": "SICGEN", "url": "https://sicgen.pt/", "image": f"{common_file_path_for_partners_image_data}/Sicgen_antibodies.png"},
    {"name": "Sino Biological", "url": "https://www.sinobiological.com/", "image": f"{common_file_path_for_partners_image_data}/Sino-Biological.png"},
    {"name": "Niels Danbolt University of Oslo", "url": "https://www.uio.no/", "image": f"{common_file_path_for_partners_image_data}/University_of_Oslo.png"},
    {"name": "NIH", "url": "https://www.nhpreagents.org/", "image": f"{common_file_path_for_partners_image_data}/NIH.png"},
    {"name": "ichorbio", "url": "https://ichor.bio/", "image": f"{common_file_path_for_partners_image_data}/ichorbio.png"},
    {"name": "Antibodies Incorporated", "url": "https://www.antibodiesinc.com/", "image": f"{common_file_path_for_partners_image_data}/antibodies_incorporated.jpg"},
    {"name": "HUABIO", "url": "https://www.huabio.com/", "image": f"{common_file_path_for_partners_image_data}/HUABIO.png"},
    {"name": "NanoTag", "url": "https://nano-tag.com/", "image": f"{common_file_path_for_partners_image_data}/NanoTag.jpg"},
    {"name": "Institute for Protein Innovation", "url": "https://proteininnovation.org/", "image": f"{common_file_path_for_partners_image_data}/Institute_for_Protein_Innovation.png"},
    {"name": "Fujirebio", "url": "https://www.fujirebio.com/en", "image": f"{common_file_path_for_partners_image_data}/Fujirebio.jpeg"},
    {"name": "Boster Biological Technology", "url": "https://www.bosterbio.com/", "image": f"{common_file_path_for_partners_image_data}/Boster_Biological-logo.png"},
    {"name": "Fujifilm Wako USA", "url": "https://wakousa.com/", "image": f"{common_file_path_for_partners_image_data}/fujifilm-wako-chemicals-usa-corporation-logo-vector.png"},
    {"name": "Active Motif", "url": "https://www.activemotif.com/", "image": f"{common_file_path_for_partners_image_data}/Active-Motif.jpg"},
    {"name": "Life Canvas Technologies", "url": "https://lifecanvastech.com/", "image": f"{common_file_path_for_partners_image_data}/LifeCanvas.jpeg"},
    {"name": "AdipoGen Life Sciences", "url": "https://adipogen.com/", "image": f"{common_file_path_for_partners_image_data}/AdipoGen_Logo_LIFE_SCIENCES_CMYK_2015_NEW_13cm_lowres.jpg"},
    {"name": "Creative Biolabs", "url": "https://www.creativebiolabs.net/?utm_source=antibodyregistry&utm_medium=logo&utm_campaign=Creative+Biolabs-Recombinant+Antibody", "image": f"{common_file_path_for_partners_image_data}/biolabs.png"},
    {"name": "Bio-techne", "url": "https://www.bio-techne.com/", "image": f"{common_file_path_for_partners_image_data}/bio-techne.png"},
    {"name": "Bio-Rad", "url": "https://www.bio-rad.com/", "image": f"{common_file_path_for_partners_image_data}/bio-rad.jpg"}
]

def add_partners(apps, schema_editor):
    Partner = apps.get_model('api', 'Partner')
    for partner in partners:
        if partner.get("image"):
            image_path = partner["image"]
            with open(image_path, 'rb') as image_file:
                Partner.objects.create(
                    name=partner["name"],
                    url=partner["url"],
                    image=File(image_file, name=os.path.basename(image_path))
                )
        else:
            Partner.objects.create(
                name=partner["name"],
                url=partner["url"]
            )

class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_add_partner_model"),
    ]

    operations = [
        migrations.RunPython(add_partners),
    ]