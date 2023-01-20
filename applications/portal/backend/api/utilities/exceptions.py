from openapi.models import Antibody as AntibodyDTO


class DuplicatedAntibody(Exception):
    def __init__(self, antibody: AntibodyDTO):
        super().__init__("Antibody exists")
        self.antibody = antibody


class RequiredParameterMissing(Exception):
    def __init__(self, parameter):
        super().__init__(f"{parameter} missing")

class AntibodyDataException(Exception):
    def __init__(self, message, field_name, field_value):
        super().__init__(message)
        self.field_name = field_name
        self.field_value = field_value


class NonexistingSubmitter(Exception):
    def __init__(self, submitter_id: str, antibody: AntibodyDTO):
        super().__init__(f"Submitter {submitter_id} does not exists for antibody {antibody}")
        self.submitter_id = submitter_id
        self.antibody = antibody