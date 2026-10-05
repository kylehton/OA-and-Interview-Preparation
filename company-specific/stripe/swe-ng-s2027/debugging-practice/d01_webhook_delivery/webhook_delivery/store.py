class MemoryEventStore:
    def __init__(self) -> None:
        self._processed: set[str] = set()

    def is_processed(self, event_id: str) -> bool:
        return event_id in self._processed

    def mark_processed(self, event_id: str) -> None:
        self._processed.add(event_id)

