# Default KC roles
KC_ADMIN_ROLE = f"portal:administrator"  # admin user
KC_MANAGER_ROLE = f"portal:manager"  # manager user
KC_USER_ROLE = f"user"  # customer user
KC_ALL_ROLES = [
    KC_ADMIN_ROLE,
    KC_MANAGER_ROLE,
    KC_USER_ROLE,
]
KC_PRIVILEGED_ROLES = [
    KC_ADMIN_ROLE,
    KC_MANAGER_ROLE,
]

KC_DEFAULT_USER_ROLE = None  # don't add the user role to the realm default role

# Database models settings
IMPORT_EXPORT_USE_TRANSACTIONS = True

# comment refers to max length of column at ingestion time (12/09/2022)
ANTIBODY_NAME_MAX_LEN = 512  # 352
ANTIBODY_TARGET_MAX_LEN = 1024  # 783
ANTIBODY_TARGET_SPECIES_MAX_LEN = 4096  # 2047
VENDOR_MAX_LEN = 512  # 200
ANTIBODY_CATALOG_NUMBER_MAX_LEN = 256  # 165
ANTIBODY_CLONALITY_MAX_LEN = 32
ANTIBODY_CLONE_ID_MAX_LEN = 256  # 150
URL_MAX_LEN = 2048  # 938
ANTIGEN_ENTREZ_ID_MAX_LEN = 2048  # 1383
ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN = 256  # 150
ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN = 512  # 285
ANTIBODY_PRODUCT_FORM_MAX_LEN = 1024  # 802
ANTIBODY_TARGET_SUBREGION_MAX_LEN = 256  # 221
ANTIBODY_TARGET_MODIFICATION_MAX_LEN = 128  # 67
ANTIBODY_DEFINING_CITATION_MAX_LEN = 16384  # 9206
ANTIBODY_DISC_DATE_MAX_LEN = 128  # 85
ANTIBODY_ID_MAX_LEN = 32  # 8
ANTIBODY_UID_MAX_LEN = 256
STATUS_MAX_LEN = 8
ANTIBODY_CAT_ALT_MAX_LEN = 512  # 334
VENDOR_COMMERCIAL_TYPE_MAX_LEN = 32  # 10
ANTIGEN_UNIPROT_ID_MAX_LEN = 255  # 32
ANTIBODY_TARGET_EPITOPE_MAX_LEN = 1024  # 897
VENDOR_NIF_MAX_LEN = 32  # 14
VENDOR_EU_ID_MAX_LEN = 255
APPLICATION_MAX_LEN = 255
ANTIBODY_FILE_DISPLAY_NAME_MAX_LEN = 256
ANTIBODY_FILES_HASH_MAX_LEN = 32
ANTIBODY_FILE_TYPE_MAX_LEN = 32


ANTIBODY_ANTIBODY_START_SEQ = 3000000  # 2858735
ANTIBODY_VENDOR_DOMAIN_START_SEQ = 2000  # 813
ANTIBODY_VENDOR_START_SEQ = 20000  # 12233
ANTIBODY_FILE_START_SEQ = 10000  # 7001

RAW_ANTIBODY_DATA_BASENAME = 'antibody_table'
RAW_VENDOR_DATA_BASENAME = 'antibody_vendors'
RAW_VENDOR_DOMAIN_DATA_BASENAME = 'antibody_vendors_domain'
RAW_USERS_DATA_BASENAME = 'users_antibody'
RAW_ANTIBODY_FILES_BASENAME = 'antibody_files'

CHUNK_SIZE = 10 ** 4

UID_KEY = 'uid'
GUID_KEY = 'guid'

# Used for data import/export processing
ANTIBODY_HEADER = {'ab_name': "text", 'ab_target': "text", 'target_species': "text", 'vendor': "text",
                   'vendor_id': "int", 'catalog_num': "text", 'clonality': "text",
                   'source_organism': "text", 'clone_id': "text", 'url': "text", 'link': "text",
                   'ab_target_entrez_gid': "text", 'product_isotype': "text",
                   'product_conjugate': "text", 'product_form': "text", 'target_subregion': "text",
                   'target_modification': "text", 'comments': "text",
                   'feedback': "text", 'defining_citation': "text", 'disc_date': "text", 'curator_comment': "text",
                   'id': "text", 'ab_id': "text", 'ab_id_old': "text",
                   'of_record': "text", 'ix': "int", UID_KEY: "text", 'status': "text",
                   'insert_time': "text", 'curate_time': "text", 'cat_alt': "text", 'commercial_type': "text",
                   'uniprot_id': "text", 'epitope': "text", 'uid_legacy': "text", 'catalog_num_search': "text"}

D_TYPES = ANTIBODY_HEADER.copy()
for dt in D_TYPES:
    if dt == 'int':
        D_TYPES[dt] = 'int64'
    else:
        D_TYPES[dt] = 'unicode'

MAX_TRIES = 10

ORCID_URL = "https://orcid.org/"
PROVIDER_ID = 'orcid'

USERS_RELEVANT_HEADER = ['id', GUID_KEY, 'email', 'level', 'firstName', 'middleInitial', 'lastName', 'organization',
                         'created', 'orcid_id']

UID_INDEX = list(ANTIBODY_HEADER.keys()).index(UID_KEY)
GUID_INDEX = USERS_RELEVANT_HEADER.index(GUID_KEY)
EMAIL_INDEX = USERS_RELEVANT_HEADER.index('email')

DEFAULT_UID = '43'

# Search limit for Antibodies for returning without ranking
LIMIT_NUM_RESULTS = 10000

FILTERABLE_FIELDS = [
    'ab_id', 'ab_name', 'accession', 
    'species', 'applications', 'ab_target',
    'clonality', 'comments', 'clone_id',
    'vendor', 'source_organism', 'catalog_num'
]

FOREIGN_OR_M2M_FIELDS = ["vendor", "applications", "species", "source_organism"]

FOR_NEW_KEY = 'for_new'
FOR_EXTANT_KEY = 'for_extant'
METHOD_KEY = 'method'
IGNORE_KEY = 'ignore'
INSERT_KEY = 'insert'
UPDATE_KEY = 'update'
DUPLICATE_KEY = 'duplicate'
OVERRIDE_KEY = 'override'
FILL_KEY = 'fill'
SKIP_KEY = 'skip'
ID_KEY = 'id'
IX_KEY = 'ix'
KC_USER_ID_KEY = 'keycloak_user'
USER_KEY = 'user'
REMOVE_KEYWORD = 'remove'

ANTIBODY_PERSISTENCE = 'antibodies'
