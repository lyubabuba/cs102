import dataclasses
import math
import time
import typing as tp

from vkapi import config, session
from vkapi.exceptions import APIError
from vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    vk_config = {
        "token": "d806c8a33647ce3d1297f7e0738c8f2963b7d14eed3f75c49990d52ca11b16670842426025451a1ea4b2a",
        "client_id": "8137477",
        "version": "5.131",
        "domain": "https://api.vk.com/method/",
    }
    domain = Session(vk_config["domain"])
    try:
        req = domain.get(
            "friends.get",
            params={
                "access_token": vk_config["token"],
                "v": vk_config["version"],
                "user_id": str(user_id),
                "offset": str(offset),
                "count": str(count),
                "fields": fields,
            },
        )
        data = req.json()["response"]["items"]
        count = req.json()["response"]["count"]
        return FriendsResponse(count, list(data))
    except:
        pass
    return FriendsResponse(0, [{"items": ""}])


class MutualFriends(tp.Dict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    vk_config = {
        "token": "a3834712a2f44f6020dd1ebb6efaa6696b5b19acd878adfa1a95ab78df8595766331a2cae7080549b2dab",
        "client_id": "8094474",
        "version": "5.131",
        "domain": "https://api.vk.com/method/",
    }
    domain = Session(vk_config["domain"])
    target_uids = [] if target_uids is None else target_uids
    if target_uid is not None:
        target_uids.append(target_uid)
    if not target_uids:
        return target_uids  # type: ignore
    cycles = (len(target_uids) - 1) // 100 + 1
    mutual_friends = []
    for i in range(cycles):
        user_ids = ""
        for j in range(i * 100, i * 100 + 100 if i != cycles - 1 else len(target_uids) % 100):
            user_ids = user_ids + "," + str(target_uids[j])
        user_ids = user_ids[1 : len(user_ids)]
        try:
            req = domain.get(
                "friends.getMutual",
                params={
                    "access_token": vk_config["token"],
                    "v": vk_config["version"],
                    "source_uid": str(source_uid),
                    "target_uids": str(user_ids),
                    "offset": str(i * 100),
                    "order": order,
                    "count": 100,
                },
            )
            for item in req.json()["response"]:
                mutual_friends.append(
                    MutualFriends(
                        id=item["id"],
                        common_count=item["common_count"],
                        common_friends=item["common_friends"],
                    )
                )
        except:
            pass
        time.sleep(0.35)
    if len(mutual_friends) == 1:
        return mutual_friends[0]["common_friends"]
    return mutual_friends


if __name__ == "__main__":
    print(get_friends(335415806))
    print(get_mutual(source_uid=335415806, target_uids=[469126965, 170103551]))
