import requests
import execjs


def getSongInfo(songname):
    # 得到搜索信息
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    params = ctx.call('keySet', songname)
    data = {
        'params': params['encText'],
        'encSecKey': params['encSecKey']
    }
    # 得到的所有歌曲信息
    response = requests.post(url, data=data, headers=headers)
    # 得到所有的歌曲信息
    songinfo = response.json()['result']['songs']
    song_name_list = []
    song_id_list = []
    # 提取前三首的id
    for i in range(3):
        id = songinfo[i]['id']
        name = songinfo[i]['ar'][0]['name']
        song_id_list.append(id)
        song_name_list.append(name)
    return song_id_list, song_name_list


def geturl(songid):
    url_list = []
    for i in range(3):
        id = songid[i]
        # 请求url
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        params = ctx.call('params', id)
        data = {
            'params': params['encText'],
            'encSecKey': params['encSecKey']
        }
        response = requests.post(url, data=data, headers=headers).json()
        geturl = response['data'][0]['url']
        url_list.append(geturl)
    return url_list


if __name__ == '__main__':
    # 得到前三首歌的音乐id
    songid, songname = getSongInfo(input("请输入歌曲名字:\n"))
    urls = geturl(songid)
    for i in range(3):
        if (urls[i]):
            print(songname[i] + "\t\t\t" + urls[i])
