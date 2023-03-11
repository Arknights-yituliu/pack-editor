from ninja import Router, Schema
from typing import List
from .models import Pack, GachaList, DevelopList, OtherList

router = Router()


class ContentSchema(Schema):
    packContentItem: str
    packContentQuantity: int


class PackSchema(Schema):
    packName: str
    packShowName: str
    packImg: str
    packID: int
    packPrice: int
    packType: str
    packState: int
    gachaOriginium: int
    packDraw: float
    gachaPermit: int
    gachaPermit10: int
    gachaOrundum: int
    packRmbPerDraw: float = None
    packOriginium: float
    packRmbPerOriginium: float
    packPPRDraw: float
    packPPROriginium: float
    packContent: List[ContentSchema]
    packTag: str = None


class ResponseSchema(Schema):
    code: int
    msg: str
    data: List[PackSchema]


@router.get("/", response=ResponseSchema)
def list_packs(request):
    rpd_648 = 0
    rpo_648 = 0

    data = []
    for pack in Pack.objects.all():
        glqs = GachaList.objects.filter(pack=pack)
        gacha_sum = sum([gl.gacha_resource.orundum * gl.count for gl in glqs])
        packDraw = gacha_sum / 600 + pack.originium * 0.3
        try:
            gachaPermit = glqs.get(gacha_resource__name="单抽").count
        except:
            gachaPermit = 0
        try:
            gachaPermit10 = glqs.get(gacha_resource__name="十连").count
        except:
            gachaPermit10 = 0
        try:
            gachaOrundum = glqs.get(gacha_resource__name="合成玉").count
        except:
            gachaOrundum = 0
        packRmbPerDraw = pack.price / packDraw if packDraw else None

        dlqs = DevelopList.objects.filter(pack=pack)
        dl_list = [
            {
                "packContentItem": dl.develop_resource.name,
                "packContentQuantity": dl.count,
            }
            for dl in dlqs
        ]
        develop_sum = sum([dl.develop_resource.value * dl.count for dl in dlqs])
        oiqs = OtherList.objects.filter(pack=pack)
        oi_list = [
            {
                "packContentItem": oi.other_item.name,
                "packContentQuantity": oi.count,
            }
            for oi in oiqs
        ]
        other_sum = sum([oi.other_item.originium * oi.count for oi in oiqs])
        packOriginium = pack.originium + gacha_sum / 180 + develop_sum / 135 + other_sum
        packRmbPerOriginium = pack.price / packOriginium

        if pack.name == "普通源石648元":
            rpd_648 = packRmbPerDraw
            rpo_648 = packRmbPerOriginium

        packTag = note if (note := pack.note) else None
        data.append(
            {
                "packName": pack.name,
                "packShowName": pack.name,
                "packImg": pack.name,
                "packID": pack.pack_id,
                "packPrice": pack.price,
                "packType": Pack.Limitation(pack.limitation).label,
                "packState": pack.on_sale,
                "gachaOriginium": pack.originium,
                "packDraw": packDraw,
                "gachaPermit": gachaPermit,
                "gachaPermit10": gachaPermit10,
                "gachaOrundum": gachaOrundum,
                "packRmbPerDraw": packRmbPerDraw,
                "packContent": dl_list + oi_list,
                "packOriginium": packOriginium,
                "packRmbPerOriginium": packRmbPerOriginium,
                "packTag": packTag,
            }
        )
    for i in data:
        i["packPPRDraw"] = (
            rpd_648 / packRmbPerDraw if (packRmbPerDraw := i["packRmbPerDraw"]) else 0
        )
        i["packPPROriginium"] = rpo_648 / i["packRmbPerOriginium"]
    return {
        "code": 200,
        "msg": "操作成功",
        "data": data,
    }
