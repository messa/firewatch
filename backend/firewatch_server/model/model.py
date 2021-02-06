from collections import defaultdict
from logging import getLogger


logger = getLogger(__name__)


class Model:

    def __init__(self):
        self.check_results = defaultdict(list) #

    async def store_check_result(self, check, result):
        assert result.status_ok in (True, False)
        self.check_results[check.check_id].append(result)
        while len(self.check_results[check.check_id]) >= 1000:
            self.check_results[check.check_id].pop(0)

    async def get_last_check_result(self, check):
        results = self.check_results.get(check.check_id)
        if results:
            return results[-1]
        else:
            return None

    async def get_last_check_results(self, check, limit=25):
        results = self.check_results.get(check.check_id)
        if results:
            return list(reversed(results[-limit:]))
        else:
            return []
