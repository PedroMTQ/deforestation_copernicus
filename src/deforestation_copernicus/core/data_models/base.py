from dataclasses import fields, dataclass, asdict

@dataclass
class BaseDataModel():
    @classmethod
    def from_dict(cls, data_dict: dict):
        res = {}
        cls_fields = [f.name for f in fields(cls)]
        for k, v in data_dict.items():
            if k in cls_fields:
                res[k] = v
        return cls(**res)

    def to_dict(self) -> dict:
        return asdict(self)
