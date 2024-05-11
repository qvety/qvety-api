from bitfield.types import BitHandler
from pydantic import BaseModel


class BitSetData(BaseModel):
    value: str
    label: str


def get_set_data(self) -> list[BitSetData]:
    selected_flags = [BitSetData(value=k, label=self.get_label(k)) for k in self._keys if getattr(self, k).is_set]
    return selected_flags


BitHandler.get_set_data = get_set_data
