from app.db.mongo_utils import MongoCrud
from app.schema import video_chapters as video_chapter_schema


class VideoChapterModel(MongoCrud[video_chapter_schema.VideoChapterDocument]):
    model = video_chapter_schema.VideoChapterDocument