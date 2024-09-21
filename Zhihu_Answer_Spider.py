# 程序功能: 爬知乎回答
# 程序作者: 马哥python说
import requests
import time
import pandas as pd
import os
import re
import random

# 请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'cookie':'_xsrf=FqaNftC0rqrvXZhElvr3WnLNdQvahXWk; _zap=6a958bc4-95e2-4ef2-8c49-9c8febe3668b; d_c0=ADDSiI4_ExmPTuDixT-MvklE5iW6nWI_MtU=|1723568459; __zse_ck=003_b6ImbeZoux=qZb0pZ0aez1SzEudFXMT72lRut/8oD3vWGZunXLGG5+By1N8rKaDXLAXW61ug=kdZNavqGFrjU=tmtIisji4RLiod3+nC3PBs; captcha_session_v2=2|1:0|10:1725903941|18:captcha_session_v2|88:UXp3M0pSa3J4MUNzWjBPUXIvazlJZ0tsR1A3Qjh3TzhmcTJlTURLZ0lYWUNBTUtPSXEvT2NGYWg5cy9wVUd3UA==|cdf11daac764e14b242215a30eeb1c7e9373d798a14665a406f8324e9b33a128; __snaker__id=iM0rM3cXkyQNyKW7; gdxidpyhxdE=kvx6r2yIUx9PJwIHo88wp86cAukToi%2F7PLizd4zp4kqDuUpYSaUyKiN8Aj3yWjZCXWWrqdspouQx%5CPUbK0bB4HAp965pahQbs8MnA%2F32UvCXChajLcIG1rBNiDPeYAziYgmde4kE2iU5QlgeP%2Fu21vLI8k5NHsMjcjw%5CNYrKGoojyOgn%3A1725904847188; captcha_ticket_v2=2|1:0|10:1725903959|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfem5CaVlRZnhUcmN5ZjZoSF92KlMwaTZlQ1NHdkNaZDZ0YmdOREZwWW0yWEJlbnJMc0VUUlhqeGRMVnU4Q3hLZDVTUktGNG4yXzVqZkJvbnlOYThMUng1RGI5R3lPQ0lUa2VObkN6TF9jU1FKa1EzVWZ3SzNuQjU1bkJGRk5DdEEzM1NJU0Z5MW4yY0hvNjAuNHE5UlkwOWNUSWx1Km0qRktybGpxQ3pfaVpVMUpLMWJwazZNdEg2SkQ5dklTaUNOM1J1RmVtcXVQQ3dyd0hNU2dra0hnWUN2Tl9hdEFLczZPczk5cldNbUlBRzVWeFgwdGxXWFcyWVd2cXRkMlBobS5MNmlGUFUwbnVoUVN3OFVfMjFMMkJDUlVoTzZOVGUyeXVycElxUUJTOUYzM0pEX0NWT0l6V2JXdjltSEdid25nb2FYbVNuOUNiNXpUaHpJVzExdU5aNjZ5TXl2aFU5aVhqZDU2OVZUQjBiMjJDMGZRcnJRQlYqX1NZMUxGVi5GcUNITUlwRTlaeFU1X0hwc0xSZWRiQzZrMmN4ZkhvekpfKkNMWG5jVEh4LjBjOEl0ZUtKaVVvbm9ZVzEzWm5zbUZlamVTTWpiaVQqVkk5MGxBcSoyUzNlLnFyU1c2SXhaRHd4TndNVzlGNWlsQjhTVVRiUUFxcFBwbjBmdXJIdmFXdkpJRk03N192X2lfMSJ9|889de4bd92f4792cd17a07405d38baeeb1319f3ea7470bd9630520782974f18e; z_c0=2|1:0|10:1725904060|4:z_c0|92:Mi4xVzhwSFZRQUFBQUFBTU5LSWpqOFRHU1lBQUFCZ0FsVk52SUxNWndCdm5PVWxkdnhzTGtVOTJzd0ZDYVN5Y2VONnBn|428c90bb2a84a16d3c9ccac126ba32b1e0d7854f183fc860c5fd7486e723f299; q_c1=3345dc477b6541319de55367dd25e12d|1725904060000|1725904060000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1725709786,1725903940,1725906847,1725949116; HMACCOUNT=41D79DCB76C3959C; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1725949222; BEC=f7bc18b707cd87fca0d61511d015686f',
}


def trans_date(v_timestamp):
    """10位时间戳转换为时间字符串"""
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def tran_gender(gender_tag):
    """转换性别"""
    if gender_tag == 1:
        return '男'
    elif gender_tag == 0:
        return '女'
    else:  # -1
        return '未知'


def clean_content(v_text):
    """回答内容数据清洗"""
    dr = re.compile(r'<[^>]+>', re.S)
    text2 = dr.sub('', v_text)
    return text2


def answer_spider(v_result_file, v_question_id):
    # 请求地址
    url = 'https://www.zhihu.com/api/v4/questions/{}/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop'.format(
        v_question_id)
    while True:
        # 发送请求
        r = requests.get(url, headers=headers)
        # 接收返回数据
        j_data = r.json()

        # Print paging info for debugging
        # print("Paging Info:", j_data['paging'])

        answer_list = j_data['data']
        # 定义空列表用于存数据
        author_name_list = []  # 答主昵称
        author_gender_list = []  # 答主性别
        follower_count_list = []  # 答主粉丝数
        author_url_list = []  # 答主主页
        headline_list = []  # 答主签名
        answer_id_list = []  # 回答id
        answer_time_list = []  # 回答时间
        answer_content_list = []  # 回答内容
        comment_count_list = []  # 评论数
        voteup_count_list = []  # 点赞数
        thanks_count_list = []  # 喜欢数
        is_end = j_data['paging']['is_end']  # 是否最后一页
        page = j_data['paging']['page']
        print('开始爬取第{}页，本页回答数量是：{}'.format(page, len(answer_list)))
        time.sleep(random.uniform(0, 1))
        for answer in answer_list:
            # 答主昵称
            author_name = answer['target']['author']['name']
            author_name_list.append(author_name)
            # 答主性别
            author_gender = answer['target']['author']['gender']
            author_gender = tran_gender(author_gender)
            author_gender_list.append(author_gender)
            # 答主粉丝数
            try:
                follower_count = answer['target']['author']['follower_count']
            except:
                follower_count = ''
            follower_count_list.append(follower_count)
            # 答主主页
            author_url = 'https://www.zhihu.com/people/' + answer['target']['author']['url_token']
            author_url_list.append(author_url)
            # 答主签名
            headline = answer['target']['author']['headline']
            headline_list.append(headline)
            # 回答id
            answer_id = answer['target']['id']
            answer_id_list.append(answer_id)
            # 回答时间
            answer_time = answer['target']['updated_time']
            answer_time = trans_date(answer_time)
            answer_time_list.append(answer_time)
            # 回答内容
            try:
                answer_content = answer['target']['content']
                answer_content = clean_content(answer_content)
            except:
                answer_content = ''
            answer_content_list.append(answer_content)
            # 评论数
            comment_count = answer['target']['comment_count']
            comment_count_list.append(comment_count)
            # 点赞数
            voteup_count = answer['target']['voteup_count']
            voteup_count_list.append(voteup_count)
            # 喜欢数
            thanks_count = answer['target']['thanks_count']
            thanks_count_list.append(thanks_count)

        # 保存数据到csv
        if os.path.exists(csv_file):  # 如果csv存在，不写表头，避免重复写入表头
            header = False
        else:
            header = True
        # 数据保存为Dataframe格式
        df = pd.DataFrame(
            {
                '问题id': v_question_id,
                '页码': page,
                '答主昵称': author_name_list,
                '答主性别': author_gender_list,
                '答主粉丝数': follower_count_list,
                '答主主页': author_url_list,
                '答主签名': headline_list,
                '回答id': answer_id_list,
                '回答时间': answer_time_list,
                '评论数': comment_count_list,
                '点赞数': voteup_count_list,
                '喜欢数': thanks_count_list,
                '回答内容': answer_content_list,
            }
        )
        # 保存到csv文件
        df.to_csv(v_result_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
        # 判断是否退出
        if not is_end:  # 如果不是最后一页
            url = j_data['paging']['next']  # 下一页的请求地址
        else:  # 如果是最后一页
            print('is_end is True , break now!')
            break


if __name__ == '__main__':
    # 问题id
    question_id = '666543659'
    # 保存文件名
    csv_file = '知乎回答_{}.csv'.format(question_id)
    # 如果csv存在，先删除，避免由于追加产生重复数据
    if os.path.exists(csv_file):
        print('文件存在，删除：{}'.format(csv_file))
        os.remove(csv_file)
    # 开始爬取
    answer_spider(v_result_file=csv_file,  # 保存文件名
                  v_question_id=question_id,
                  )
    print('爬虫执行完毕！')
