export const faqsInfo = [
  {
    question:"Is login required for search?",
    answer:"No, searching for antibodies, sorting, faceting will never require anyone to be logged in. Simply type your favorite catalog number or other metadata item (polyclonal GFAP) into the search bar present throughout the site and begin searching.",

  },
  {
    question:"Why Login?",
    answer:"To add antibody records or to edit your submitted records you will need to be logged in."
  },
  {
    question:"How much information do I need to provide with login information?",
    answer: "When logging in you will be asked to verify your academic status using ORCID and then you will be asked to provide your email address. Providing an email allows us to write you an acceptance or rejection letter after you submit your antibody. Especially important if there is a problem with your submission."
  },
  {
    question: "Can I add antibodies without logging in?",
    answer:"Yes, please download a CSV file (link to a CSV’s with examples), fill in the required information and email to abr-help -at- scicrunch -dot- org. If you are not able to download the file please create an Excel or CSV file with the following columns: Commercial Antibody/Kit Data Fieldst: *Catalog Number*, Vendor, *Vendor Product Page Link*, Antibody Name, Host Species, Target/Reactive Species, Antibody Target, Clonality, Clone ID, Isotype, Conjugate, Antibody Form/Format, Uniprot ID, Epitope, Applications, Comments, Kit Contents Personal/Custom Antibody Data Fields: *Identifier*, *Principal Investigator - Institution *, *Principal Investigator's or Institution's Website*, *Antibody Name *, *Host Species *, *Target/Reactive Species *, *Antibody Target *, *Clonality *, Clone ID, Isotype, Conjugate, Antibody Form/Format, Uniprot ID, Epitope, Applications, Comments, Defining Citation Fields marked with * are required."
  },
  {
    question:"Can I add dyes to the antibody registry?",
    answer:"No, the Antibody Registry is only for antibodies and kits that contain antibodies. Other proteins and dyes (e.g. Streptavidin, DAPI) do not need to be registered. There are legacy records in the registry that are not antibodies. They are tagged with a 'do not use this RRID' message when found. Nanobodies, mini antibodies, fab fragments and single domain antibodies are also antibodies and are sold the same way as traditional full antibodies (both heavy and light chains)."
  },
  {
    question: "Why do you only require catalog numbers, vendor URLs?",
    answer:"Every vendor has their own way of formatting their catalog numbers. We try to reproduce those catalog numbers exactly as they are on the vendors websites. Many vendors append ‘sizing’ information to the end of their catalog numbers (-100, S, L, 50uL). We try to provide only one RRID for a product - regardless of the size. Therefore, when registering or searching for products, do not include sizing information in the catalog number, if it can be easily differentiated. We will add known sizes in the alternative catalog number field when we know about them. Vendor URLs should point to a page that contains information about the antibody being registered. If a URL with information is not available, you may be asked to provide some documentation like a technical data sheet."
  }
]