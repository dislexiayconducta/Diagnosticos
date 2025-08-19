from django.db.models import Q
from .models import TestType

_testtype_cache = {}


def get_template_type(testtype: str) -> str:
    if testtype in _testtype_cache:
        return _testtype_cache[testtype]

    try:
        test = TestType.objects.get(Q(test_id=testtype) | Q(name=testtype))
        _testtype_cache[testtype] = test.template_asigned

    except TestType.DoesNoExists:
        _testtype_cache[testtype] = "Unknown"
    return _testtype_cache[testtype]
