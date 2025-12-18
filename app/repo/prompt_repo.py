from app.repo.base_repo import BaseRepository
from app.models.prompt import Prompt


class PromptRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(Prompt, db)

    async def get_storyboard_by_file_and_video(self, file_id, video_number):
        result = await self.db.execute(
            self.model.__table__
            .select()
            .where(self.model.file_id == file_id)
            .where(self.model.video_number == video_number)
        )
        row = result.fetchone()
        return row.prompt if row else None
