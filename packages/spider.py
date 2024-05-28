import requests
import time
import pandas as pd
import os
import random
from packages.utils import trans_date, trans_gender, clean_content

# 请求头 / Header
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'cookie': r'_zap=6be4b7a3-82bb-4d75-ba18-7663baac9ba3; _xsrf=3c9b56fa-f096-406d-9462-703733cfd8d4; d_c0=ADDf18H6rxiPTr3N1AupukTN2q3eyiesmrQ=|1716906646; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1716906650; BEC=d5e2304fff7e4240174612484fe7ffa4; captcha_session_v2=2|1:0|10:1716906651|18:captcha_session_v2|88:SVRuWWd6anYwMC9sWjEvZXFlK0loT3hZQndMTHl1NktiUUZRekJxOEw3UnA4S1BOVHRRUkg2Z2FZQ3ppZ01aVA==|c1531d9d1729ced6c991072c51092c641ad8c673278e3fbbbdce0ed083994ee8; gdxidpyhxdE=1V6TQL7SbCB8DcIVsD6W2uSH8nkO%2B1mJIrVhU3h9zBVnHHzIPvAXEmIUm%5CO%2F%5CKhVYcypIm%5CzEyNClonLrG9rJzrZpPQviLG%2FOfJscYCW%2FVHTv%2FPiLO%2FuCLIZhJ9zOAyouY1RyW14%2Fq%2BqkpqMXMJWqIczS5%2BCq1dIoEHaKMO3K0M3rPd2%3A1716907557707; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1716906669; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1716906668|1716906646'
}

def answer_spider(v_result_file, v_question_id):
    # 请求地址/URL
    url = 'https://www.zhihu.com/api/v4/questions/{}/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop'.format(
        v_question_id)
    if os.path.exists(v_result_file):
        print("File '{}' already exists. Skipping scraping for question ID: {}".format(v_result_file, v_question_id))
        return
    while True:
        # 发送请求/Request
        r = requests.get(url, headers=headers)
        if r.status_code == 404:
            print(f"Question ID {v_question_id} does not exist.")
            return
        # 接收返回数据/Return the Data
        j_data = r.json()
        answer_list = j_data['data']
        # 定义空列表用于存数据/Define Empty List for Data
        author_name_list = []  # 答主昵称/Author_Name
        author_gender_list = []  # 答主性别/Gender
        follower_count_list = []  # 答主粉丝数/Follower_Count
        author_url_list = []  # 答主主页/Homepage
        headline_list = []  # 答主签名/Profile_Introduction
        answer_id_list = []  # 回答id/Answer_ID
        answer_time_list = []  # 回答时间/Answer_Time
        answer_content_list = []  # 回答内容/Answer
        comment_count_list = []  # 评论数/Comment_Count
        voteup_count_list = []  # 点赞数/Thumbs_Ip
        thanks_count_list = []  # 喜欢数/Likes
        is_end = j_data['paging']['is_end']  # 是否最后一页/If_Last_Page
        page = j_data['paging']['page']
        print('开始爬取第{}页，本页回答数量是：{}'.format(page, len(answer_list)))
        print('Start Crawling Page {}, Total Answers: {}'.format(page, len(answer_list)))
        time.sleep(random.uniform(0, 1))
        for answer in answer_list:
            # 答主昵称/Author_Name
            author_name = answer['target']['author']['name']
            author_name_list.append(author_name)
            # 答主性别/Gender
            author_gender = answer['target']['author']['gender']
            author_gender = trans_gender(author_gender)
            author_gender_list.append(author_gender)
            # 答主粉丝数/Follower_Count
            try:
                follower_count = answer['target']['author']['follower_count']
            except:
                follower_count = ''
            follower_count_list.append(follower_count)
            # 答主主页/Homepage
            author_url = 'https://www.zhihu.com/people/' + answer['target']['author']['url_token']
            author_url_list.append(author_url)
            # 答主签名/Profile_Introduction
            headline = answer['target']['author']['headline']
            headline_list.append(headline)
            # 回答id/Answer_ID
            answer_id = answer['target']['id']
            answer_id_list.append(answer_id)
            # 回答时间/Timestamp
            answer_time = answer['target']['updated_time']
            answer_time = trans_date(answer_time)
            answer_time_list.append(answer_time)
            # 回答内容/Content
            try:
                answer_content = answer['target']['content']
                answer_content = clean_content(answer_content)
            except:
                answer_content = ''
            answer_content_list.append(answer_content)
            # 评论数/Comment_Count
            comment_count = answer['target']['comment_count']
            comment_count_list.append(comment_count)
            # 点赞数/Thumbs_Up
            voteup_count = answer['target']['voteup_count']
            voteup_count_list.append(voteup_count)
            # 喜欢数/Likes
            thanks_count = answer['target']['thanks_count']
            thanks_count_list.append(thanks_count)

        # 保存数据到csv/Saving Data to CSV
        if os.path.exists(v_result_file):  # 如果csv存在，不写表头，避免重复写入表头/If CSV exists, skip header
            header = False
        else:
            header = True
        # 数据保存为Dataframe格式/Save Data in DataFrame Format
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
        # 保存到csv文件/Save CSV
        df.to_csv(v_result_file, mode='a+', index=False, header=header, encoding='utf_8_sig')

        # 判断是否退出/If Exit
        if not is_end:  # 如果不是最后一页/If not last page
            url = j_data['paging']['next']  # 下一页的请求地址/Next Page Request
        else:  # 如果是最后一页/If last page
            print('is_end is True , break now!\n')
            break
