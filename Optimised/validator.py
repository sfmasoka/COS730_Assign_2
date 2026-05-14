

from utils import call_counter, log


class Validator:
    def validateFormat(self, data: dict) -> bool:
        call_counter.increment("Validator.validateFormat")
        log("Validator", "validateFormat(data)")

        required_fields = ["title", "author", "content"]
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                log("Validator", f"Validation FAILED — missing or empty field: '{field}'")
                return False

        log("Validator", "Validation PASSED")
        return True
