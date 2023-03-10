from ninja import Router, Schema, Field
from typing import List
from .models import GachaResource, DevelopResource, OtherItem, Pack, GachaList

router = Router()


class PackSchema(Schema):
    packName: str = Field(..., alias="name")
    packShowName: str = Field(..., alias="name")
    packImg: str = Field(..., alias="name")
    packID: int = Field(..., alias="pack_id")
    packPrice: int = Field(..., alias="price")
    packType: str
    packState: int = Field(..., alias="on_sale")
    gachaOriginium: int = Field(..., alias="originium")
    packDraw: float
    gachaPermit: int
    gachaPermit10: int
    # gachaOrundum: int
    # packPPRDraw: float
    # packPPROriginium: float
    # packRmbPerOriginium: float
    # packOriginium: float
    # packRmbPerDraw: float

    @staticmethod
    def resolve_packType(obj):
        return Pack.Limitation(obj.limitation).label

    @staticmethod
    def resolve_gachaPermit(obj):
        try:
            return (
                GachaList.objects.filter(pack=obj).get(gacha_resource__name="单抽").count
            )
        except:
            return 0

    @staticmethod
    def resolve_gachaPermit10(obj):
        try:
            return (
                GachaList.objects.filter(pack=obj).get(gacha_resource__name="十连").count
            )
        except:
            return 0

    @staticmethod
    def resolve_packDraw(obj):
        return (
            sum(
                [
                    gl.gacha_resource.orundum * gl.count
                    for gl in GachaList.objects.filter(pack=obj)
                ]
            )
            / 600
            + obj.originium * 0.3
        )


class ResponseSchema(Schema):
    code: int
    msg: str
    data: List[PackSchema]


@router.get("/", response=ResponseSchema)
def list_packs(request):
    return {
        "code": 200,
        "msg": "操作成功",
        "data": list(Pack.objects.all()),
    }
