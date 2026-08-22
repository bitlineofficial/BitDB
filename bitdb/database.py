import json
from pathlib import Path

from .collection import Collection


class Database:
    def __init__(self, path: str):
        self.path = Path(path)
        self.create_database()
        self.data = self._load()
        

    def create_database(self) -> None:
        
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")


    def _load(self) -> dict:
        
        with self.path.open("r", encoding="utf-8") as data:
            return json.load(data)
            

    def _save(self) -> None:
        
        with self.path.open("w", encoding="utf-8") as data:
            json.dump(self.data,
                      data,
                      ensure_ascii=False,
                      indent=4)




    def collection(
        self,
        name: str,
        unique_fields: list[str] | None = None
    ) -> Collection:

        self.data.setdefault(name, [])
        self._save()

        return Collection(
            name,
            self,
            unique_fields
        )



    def collections(self) -> list[str]:
        return list(self.data.keys())



    def delete_collection(self, name: str) -> bool:
        if name not in self.data:
            return False
        
        del self.data[name]
        self._save()
        
        return True