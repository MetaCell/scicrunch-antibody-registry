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


class AntibodyDoesNotExist(Exception):
    def __init__(self, antibody_id):
        super().__init__(f"Antibody with id {antibody_id} does not exist")
        self.antibody_id = antibody_id


class FetchCitationMetricFailed(Exception):
    def __init__(self, ab_id):
        super().__init__(f"Failed to fetch citation metrics for {ab_id}")
