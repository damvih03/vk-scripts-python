import requests
import os


class VkApi:
    __version = 5.131

    def __init__(self, token: str):
        self.__token = token

    def __send_request(self, method: str, params: dict) -> dict:
        params.update({
            "access_token": self.__token,
            'v': self.__version
        })
        response = requests.post("https://api.vk.com/method/" + method, params=params)
        if response.ok:
            response = response.json()
        else:
            raise KeyboardInterrupt
        if response["response"]:
            return response["response"]
        else:
            print(response["error"])
            raise KeyboardInterrupt("API error")

    def __get_all_items(self, method: str, params: dict) -> list:
        response = self.__send_request(method, params)
        items = response["items"]
        count = response["count"]
        for offset in range(1000, count, 1000):
            params.update({"offset": offset})
            items += self.__send_request(method, params)["items"]
        return items

    def get_members(self, owner_id: int) -> list:
        """
        The method returns full members list of the group
        :param owner_id:
        :return:
        """
        method = "groups.getMembers"
        params = {
            "group_id": owner_id,
            "count": 1000,
            "sort": "id_asc",
            "offset": 0,
        }
        return self.__get_all_items(method, params)

    def photos_get(self, owner_id: int, album_id: int) -> list:
        method = "photos.get"
        params = {
            "owner_id": -owner_id,
            "album_id": album_id,
            "photo_sizes": 1,
            "count": 1000,
            "rev": 0,
            "offset": 0,
        }
        return self.__get_all_items(method, params)

    def likes_get_list(self, owner_id: int, type_object: str, item_id: int) -> list:
        method = "likes.getList"
        params = {
            "type": type_object,
            "owner_id": -owner_id,
            "item_id": item_id,
            "count": 1000,
            "offset": 0,
        }
        return self.__get_all_items(method, params)