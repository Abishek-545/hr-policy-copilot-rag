from collections import Counter
from time import perf_counter


class AnalyticsStore:
    def __init__(self) -> None:
        self.questions_asked = 0
        self.total_response_time = 0.0
        self.document_hits: Counter[str] = Counter()
        self.category_hits: Counter[str] = Counter()

    def record_question(self, elapsed_seconds: float, documents: list[str], category: str) -> None:
        self.questions_asked += 1
        self.total_response_time += elapsed_seconds
        self.document_hits.update(documents)
        if category:
            self.category_hits.update([category])

    @property
    def average_response_time(self) -> float:
        if self.questions_asked == 0:
            return 0.0
        return round(self.total_response_time / self.questions_asked, 2)


analytics_store = AnalyticsStore()


def timer_start() -> float:
    return perf_counter()


def timer_elapsed(start: float) -> float:
    return perf_counter() - start
