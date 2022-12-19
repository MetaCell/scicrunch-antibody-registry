from openapi.models import Antibody as AntibodyDTO


class DuplicatedAntibody(Exception):
    def __init__(self, antibody: AntibodyDTO):
        super().__init__("Antibody exists")
        self.antibody = antibody


class RequiredParameterMissing(Exception):
    def __init__(self, parameter):
        super().__init__(f"{parameter} missing")
