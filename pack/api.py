from ninja import Router, Schema
from typing import List
from .models import Pack, GachaList, DevelopList, OtherList
import datetime

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


def get_pack_data():
    rpd_648 = 0
    rpo_648 = 0

    data = []
    for pack in Pack.objects.all():
        on_sale = True
        if (sale_control := pack.on_sale_control) == Pack.OnSaleControl.MANUAL_ON:
            on_sale = True
        elif sale_control == Pack.OnSaleControl.MANUAL_OFF:
            # on_sale = False
            continue
        else:
            now = datetime.date.today()
            if pack.start_date and now < pack.start_date:
                on_sale = False
            elif pack.end_date and now > pack.end_date:
                # on_sale = False
                continue
            else:
                pass

        display_name = (
            display_name if (display_name := pack.display_name) else pack.name
        )
        image = image if (image := pack.image) else pack.name

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
                "packShowName": display_name,
                "packImg": image,
                "packID": pack.pack_id,
                "packPrice": pack.price,
                "packType": Pack.Limitation(pack.limitation).label,
                "packState": on_sale,
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
                "start": pack.start_date,
                "end": pack.end_date,
            }
        )
    for i in data:
        i["packPPRDraw"] = (
            rpd_648 / packRmbPerDraw if (packRmbPerDraw := i["packRmbPerDraw"]) else 0
        )
        i["packPPROriginium"] = rpo_648 / i["packRmbPerOriginium"]

    return data


@router.get("/pack/", response=ResponseSchema)
def list_packs(request):
    return {
        "code": 200,
        "msg": "操作成功",
        "data": get_pack_data(),
    }


class PackGachaSchema(PackSchema):
    start: str = None
    end: str = None
    rewardType: str


class ResponseGachaSchema(ResponseSchema):
    data: List[PackGachaSchema]


@router.get("/pack-gacha/", response=ResponseGachaSchema)
def list_packs_gacha(request):
    raw_data = get_pack_data()
    data = []
    for i in raw_data:
        if i["packPPRDraw"] == 0:
            continue
        if i["packName"] == "每月寻访组合包":
            continue
        if "普通源石" in i["packName"]:
            continue
        data.append(i)
        i["rewardType"] = "公共"
        if not i["start"]:
            i["start"] = "2000/01/01 00:00:00"
        else:
            i["start"] = i["start"].strftime("%Y/%m/%d 00:00:00")
        if not i["end"]:
            i["end"] = "2099/01/01 00:00:00"
        else:
            i["end"] = i["end"].strftime("%Y/%m/%d 00:00:00")
    return {
        "code": 200,
        "msg": "操作成功",
        "data": data,
    }
