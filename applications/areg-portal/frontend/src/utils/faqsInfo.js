export const faqsInfo = [
  {
    question: "Is login required for search?",
    answer: "No, searching for antibodies, sorting, faceting will never require anyone to be logged in. Simply type your favorite catalog number or other metadata item (polyclonal GFAP) into the search bar present throughout the site and begin searching."
  },
  {
    question: "Why Login?",
    answer: "To add antibody records or to edit your submitted records you will need to be logged in."
  },
  {
    question: "How much information do I need to provide with login information?",
    answer: "When logging in you will be asked to verify your academic status using ORCID and then you will be asked to provide your email address. Providing an email allows us to write you an acceptance or rejection letter after you submit your antibody. Especially important if there is a problem with your submission."
  },
  {
    question: "Can I add antibodies without logging in?",
    answer: `Yes, please download a CSV file (link to a CSV’s with examples), 
    fill in the required information and email to abr-help -at- scicrunch -dot- org. 
    If you are not able to download the file please create an Excel or CSV file with the following columns:<br/>
    • <u>Commercial Antibody/Kit Data Fieldst</u>: *Catalog Number*, Vendor,*Vendor Product Page Link*, Antibody Name, Host Species,
    Target/Reactive Species, Antibody Target, Clonality, Clone ID, Isotype, Conjugate, Antibody Form/Format, Uniprot ID, Epitope, Applications, Comments,Kit Contents <br/>
    • <u>Personal/Custom Antibody Data Fields</u>: *Identifier*, *Principal Investigator - Institution *, *Principal Investigator's or Institution's Website*, 
    *Antibody Name *, *Host Species *, *Target/Reactive Species *, 
    *Antibody Target *, *Clonality *, Clone ID, Isotype, Conjugate, Antibody Form/Format, Uniprot ID, Epitope, Applications, Comments, Defining Citation Fields marked with * are required.`
  },
  {
    question: "Can I add dyes to the antibody registry?",
    answer: `No, the Antibody Registry is only for antibodies and kits that contain antibodies. Other proteins and dyes (e.g. Streptavidin, DAPI) do not need to be registered. There are legacy records in the registry that are not antibodies. They are tagged with a 'do not use this RRID' message when found.</br> 
    Nanobodies, mini antibodies, fab fragments and single domain antibodies are also antibodies and are sold the same way as traditional full antibodies (both heavy and light chains).`
  },
  {
    question: "Why do you only require catalog numbers, vendor URLs?",
    answer: `Every vendor has their own way of formatting their catalog numbers. We try to reproduce those catalog numbers exactly as they are on the vendors websites. Many vendors append ‘sizing’ information to the end of their catalog numbers (-100, S, L, 50uL). We try to provide only one RRID for a product - regardless of the size. Therefore, when registering or searching for products, do not include sizing information in the catalog number, if it can be easily differentiated. We will add known sizes in the alternative catalog number field when we know about them.</br> 
    Vendor URLs should point to a page that contains information about the antibody being registered. If a URL with information is not available, you may be asked to provide some documentation like a technical data sheet.`
  },
  {
    question: "What happens if I add duplicate submission?",
    answer: "An antibody that is already registered does not need to be registered again. Sometimes a user submits a duplicate that has recently been registered and does not yet appear in the public record, this will result in a system message that states that it is a duplicate. Be assured that the curator will look at all submissions and get back to you in 1 business day (excluding <a href='https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States'> major US holidays <a/>)."
  },
  {
    question: "How do I edit my own submissions? (must be logged in)",
    answer: "If you have made an error in your submission, you can click on the 'Edit my submissions' button to make changes."
  },
  {
    question: "How can I download data?",
    answer: `<u>Humans</u>: Selecting a handful of antibodies and downloading the list is accomplished by clicking the box icon on the left of each antibody.<br/> 
    <u>Humans Bulk</u>: Downloading all data in bulk requires that you are logged into the AntibodyRegistry. A new tab opens called “Download”. The following information is provided:</br>
    • We are now providing a full csv of the more important data for the Antibody Registry. The CSV is rather large, and contains 6 columns (our ID, AB Name, Vendor, Catalog Number, Citation, and Reference). This file is updated weekly on Friday night (Pacific time).`
  },
  {
    question: "Why do you ask for my ORCID?",
    answer: "AntibodyRegistry has joined forces with ORCID. You may now log in via ORCID, or you may associate your current account with ORCID. We have experienced many issues with users from some countries not being able to log in. ORCID works in those countries and also verifies your password so you don’t need a separate password for the Antibody Registry. If you already have an account you can still use it."
  },
  {
    question: "What is the versioning policy of the antibody registry?",
    answer: "In 2022 we have opened up previously curator only fields that should help all users understand when each record was entered into the Antibody Registry and when it was last updated. In many cases there are several versions of an RRID record, available to users with the 2022 update. Each RRID has a version that is the core record and potentially other auxiliary records. Commonly records that come from vendors that are known to be the same record (Human Protein Atlas antibodies available via Sigma and Atlas Antibodies), there are consolidated and rejected that were found to be duplicate (Cell Signaling small vs large vials of the same product), there are records that appear as duplicates due to bulk actions (catalog that was received from Chemicon vs Millipore, which were consolidated under one company name). In all of these cases the resolver points to the core record (https://antibodyregistry.org/AB_#####) and will contain additional information about versions of that record if they exist."
  },
  {
    question: "What is the governance of the antibody registry?",
    answer: `The Antibody Registry was created as part of the Neuroscience Information Framework (DA039832) and created at the University of California at San Diego by Drs. Vadim Astakhov and Anita Bandrowski. Mr Davis Banks moved the Antibody Registry in 2014 to a MySQL database from ORACLE. Mr. Joseph Menke, Mr. Mason Pairish both served as the most recent curators for the registry.<br/>
    Formal governance was not established until the funding of the STTR award GM131551, under which responsibility and oversight of the registry was transferred to SciCrunch Inc. The current development team is MetaCell Inc. Under the GM144308 award the Antibody Registry will become a part of the RRIDs.org non-for-profit organization with an advisory board.`
  },
  {
    question: "Who are stakeholders in the antibody registry?",
    answer: "The major groups that the Antibody Registry brings together include antibody companies (~300 are registered & see list of partners on the About page), researchers (>10,000 registered users), and publishers (>2000 <a href='https://www.rrids.org/journals'>journals</a> contain at least one paper with at least one antibody RRID). However the problem of identifying antibodies in the scientific literature spans most of biomedicine and some of chemistry, thus nearly all biomedical researchers should be stakeholders and advocate for better antibody reagent identification."
  },
  {
    question: "How do I get information about your API / Programmatic access?",
    answer: "The Antibody Registry does not provide direct API access to the database. We utilize the work of our colleagues at the FDI Lab to provide this access to an index of the antibody data. Please go to <a href='https://scicrunch.org'>https://scicrunch.org</a> > MyAccount > API to gain access."
  },
  {
    question: "Do you have sustainability and preservation policy?",
    answer: `The Antibody Registry is maintained with public support from the NIH and membership fees of partner companies. Transfer of the database to a non-for-profit organization, stipulated as part of the GM144308 award, will ensure longer term stability.</br> 
    However if all else fails, the data licensed at CC-0 will be archived in Zenodo, the University of California San Diego Data Repository, and the California Digital Library.</br> 
    Current data are stored within Amazon S3, part of Amazon Web Services (AWS) designed to provide 99.9% durability of object over a given year/years; automated database backups happen every day in a relevant AWS S3 bucket; Data is permanently archived in a third party archival system to ensure long term data preservation. Certification of CoreTrustSeal will be sought under the GM144308 funding mechanism.`
  },
  {
    question: "Does the antibody registry use an ontology?",
    answer: "Gene/protein names, species, and other common scientific terminologies are retrieved from the NIFSTD Ontologies (https://github.com/SciCrunch/NIF-Ontology) and used in search. This ontology is maintained by the FDI Lab at the University of California San Diego."
  },
  {
    question: "How do publishers access records?",
    answer: `Antibody data can be downloaded as a CSV file (see instructions above) and accessed via the scicrunch API (see instructions above) in json and xml format. Each record in the RRID resolver is also available without login as json and xml by simply adding the .json or .xml suffix to the URL.<br/> 
    Example: https://scicrunch.org/RRID:AB_90755.json`
  },
  {
    question: "What is the licence of the antibody registry?",
    answer: `RRIDs are freely available for reuse under the CC-0 License, including several metadata fields (vendor name, catalog number, proper citation) are available to reuse at any time for any purpose.<br/> 
    Metadata granted to the Antibody Registry from the antibody companies that enables better search is freely available to search and use, but with important limitations for commercial reuse, as it is covered under the CC-NC license. Please contact abr-help -at- scicrunch -dot- org to discuss.`
  },
  {
    question: "What is the antibody data to paper relationship?",
    answer: `Some antibodies are used in scientific papers, and where authors list the RRID they used, if the submitter specifies the paper where origination of the antibody was described, or curators discover and annotate the RRID in the paper, there is a link between the antibody records and a PubMed identifier (paper).<br/> 
    Note to authors, it may take a month or more for your paper to show up as associated with your registered antibody. The delay is sometimes that closed access publications delay our curation. If your manuscript has been out for ~6 months or is in the open access literature but you do not see it associated with your antibody, please contact us (abr-help -at- scicrunch -dot- org).`
  },
  {
    question: "What is the software that runs the antibody registry?",
    answer: "The Antibody Registry codebase is in github: https://github.com/MetaCell/scicrunch-antibody-registry. Code License Apache 2.0"
  },
  {
    question: "What is the goal of the antibody registry?",
    answer: "The Antibody Registry gives researchers a way to universally identify antibodies used in their research. The Antibody Registry assigns unique and persistent identifiers to each antibody so that they can be referenced within publications. These identifiers only point to a single antibody or kit, this allows the antibody used in methods sections to be identified by both humans and machines."
  },
  {
    question: "Does the antibody registry take non-profit antibodies or just commercial and personal?",
    answer: "The Antibody Registry includes commercial and non-profit antibodies from hundreds of vendors and thousands of individual labs. If the antibody that you are using does not appear via search, please add your antibody by using the catalog number and the direct product URL of the vendor. Our curators can use the URL to find information about the antibody and technical data sheets. Home-grown antibodies may be added as well (additional information will be required). After submitting an antibody, a permanent identifier will be assigned. This identifier can be quickly traced back in the Antibody Registry. We never delete records, so even when an antibody disappears from a vendor's catalog, or is sold to another vendor, we can usually trace the provenance of that antibody."
  },
  {
    question: "What is the relationship of the antibody registry with the RRID initiative?",
    answer: "We are proud to support the Research Resource Identification, RRID, Initiative as the antibody authority. Every antibody listed in the Antibody Registry is also listed in the <a href='https://scicrunch.org/resources'>RRID portal</a>. Every antibody is also accessible via several resolving services including the RRID resolver (<a href='https://scicrunch.org/resolver/RRID:AB_90755'>example</a>)."
  },
  {
    question: "Can I download all RRIDS from the antibody registry?",
    answer: "Computational access to the Antibody Registry data please log in to download the full list of RRIDs and fully open metadata (CC-0 license). To access additional metadata for a more limited number of records computationally please use the scicrunch.org API to work with the search index."
  },
]