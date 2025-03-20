from app.db.mongo_utils import MongoCrud
from app.schema import modules as module_schema


class ModuleModel(MongoCrud[module_schema.ModuleDocument]):
    model = module_schema.ModuleDocument