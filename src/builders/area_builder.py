from typing import Sequence, Optional, List

from database.models.areas import AreaDb
from models.requests.area_models import AreaResponseModel


class AreaBuilder:

    @staticmethod
    def build_area_response(area: AreaDb, image: Optional[List[List[int]]]) -> AreaResponseModel:
        return AreaResponseModel(
            id=area.id,
            name=area.name,
            description=area.description,
            module=area.module,
            classroom=area.classroom,
            campus=area.campus,
            department=area.department,
            division=area.division,
            image=image
        )

    @staticmethod
    def build_area_list_response(area: Sequence[AreaDb], images: Sequence[Optional[List[List[int]]]]) -> \
            Sequence[AreaResponseModel]:
        area_response = []
        for area_db, image in zip(area, images):
            area_response.append(AreaBuilder.build_area_response(area_db, image))
        return area_response
