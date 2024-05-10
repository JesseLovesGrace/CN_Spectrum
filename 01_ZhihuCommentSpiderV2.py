import requests
import time
import pandas as pd
import os

# Request headers/请求头
headers = {
    'x-zse-93': '101_3_3.0',
    'x-ab-param': 'se_ffzx_jushen1=0;zr_expslotpaid=1;top_test_4_liguangyi=1;qap_question_author=0;tp_dingyue_video=0;tp_topic_style=0;tp_contents=2;qap_question_visitor= 0;pf_noti_entry_num=2;tp_zrec=1;pf_adjust=1;zr_slotpaidexp=1',
    'x-ab-pb': 'CroB1wKmBDMFdAHgBAsE4wQZBRsAaQFWBVIL5ArHAjMEEQU0DLULdQSiAwoE0QT0C58C7AqbCz8AQAG5AtgCVwTBBNoE4AsSBU8DbAThBMoCNwVRBUMA9wNFBNcLzwsqBEIEoANWDNwL9gJsAzQEBwyEAjIDFAVSBbcD6QQpBWALfQI/BY4DZAS0CvgDFQUPC1ADVwPoA9YEagGMAnIDMgU3DMwCVQUBC0cAzAQOBbQAKgI7AqED8wP0A4kMEl0AAAAAAAABAAAAAAEAAAAAAAMAAAEFAAIBAAABFQABAQEAAQAAAgAAABUBAQALAAEAAQAAAAABAAACBAABAAABAAEBAAEAAQAAAAIBAAEAAQAAAQABAAAAAQAAAAA=',
    'x-zst-81': '3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YD_ycXtucXYqK6P0E79y-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Io4cpr4w0mRPO7HoY70SfquPmz93mhDQyiqV9ebO1hwOYiiR0ELYuUrxmtDomqU7ynXtOnAoTh_PhRDSTFHOsaDH_8UYq0CN9UBFM6Hg1f_FOYrOGwBoYrgcCjBL9hvx1oCYK8CVYUBeTv6u1pgcMzwV8wwt1EbrL-UXBgvg0Z9N__vem_C3L8vCZfMS_Uhoftck1UGg0Bhw1rrXKZgcVQQeC-JLZ28eqWcOxLGo_KX3OsquLquoXxDpMUuF_ChUCCqkwe7396qOZ-Je8ADS9CqcmUuoYsq98yqLmUggYsBXfbLVL3qHMjwS_mXefOComiDSOkUOfQqX00UeBUcnXAh3mMD31bgOYSTSufuCYuDgCjqefWqHYeQSC',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'x-app-version': '6.42.0',
    'sec-ch-ua-mobile': '?0',
    'x-requested-with': 'fetch',
    'x-zse-96': '2.0_aHtyee9qUCtYHUY81LF8NgU0NqNxgUF0MHYyoHe0NG2f',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cookie': r'_zap=b21c869d-8321-42a2-b50d-5a4e9488bebb; d_c0=AMDW8KRgSRiPTsjSIM6Sy6VQOkat7X8bdYE=|1710021142; captcha_session_v2=2|1:0|10:1710021144|18:captcha_session_v2|88:RElQUFdhUFIwVDdrUkdRQy9IU1hiK2toWkVQWklCMnBXa1kvdWVCZStHMWdUWEZDWWhQbTdoM3VxZTVHVmYyaA==|6c4a235495b8b66453a806f7c3c196feff47f683240c99b1ebe4ffaabb914164; gdxidpyhxdE=lWl%2F1URkUAAirraqXQZfrSpSIzj2nb4%5CD%2BJopnByEgXiP6ox6K9OxE9cs%2BarihZGadjvXmNb%2BeI166ekOTQn0OHhKrx1H7ILgAt6SCk4fINdmAUnIt%5C%2B3ewsyc7rZDOlUOq0imR9HjklL1wdcu8QZ4HeldJ1JxCixvT2cZQWzQo0jEPp%3A1710022048693; captcha_ticket_v2=2|1:0|10:1710021226|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfeDlPd3NPNU92aXFCZDZENm9HdEJpeWM4cG8yelEwUE5PYzhuX3ozNU1CWDhyZVE4NEszd0t4QWtYai45SDBIM0VxT2dXb2IzbGloNjFWajBLZVFjMWVsSktNMGtLcDFaMEthYV9HUVlCdnEyVEJiZzBYX0JfMlR0TnBhVFY0anl6Wkwyci5wZXRGbDZzM0lmamczcU9iQ1VsR2NId3BIVU1JYkxVNXlaSGhoQ1JTcXhhcXFIRVM2RXhxM19BNkZuektoQ0lBTnBTLlljclZId3phS3Jtc1ZnYm50c1k1NE0xTm9mMllQaFBRc2Rldl8wcTFhOUlVQVphdE8zb0pRUWxCUlhvUnJjY1FnZ2wwUU9mQ1RHRjJNOWxLcmN1NGdmYmF4bGcwelZZSWRwaVpWTDZHelRXbXFYdUNrX2EyanFxX1BIeDBwMjVYQU5JUFcyRUd4R1lHVDNiT3FzM1pBY2o0dERnTU90MVU4Q0UyUHRYSUJwb2cwRkhHM3hHT3NOTHpINGFiNmdOcmtQS1B2Kk9oTmZRMHhUM2ZwTG00Qk81UWo1ZGlxWG13bV9DZFZ4SEloOSpHMlJ2VE9QRm9YclREVDRveEI5bm9scDlObSpRY0FrUktYcjJmdWRzV0JXa0ZqMkhYLjhLKipZKk16b2wqR0JENVpZMHB3dmtoYk9uOFUuSGc3N192X2lfMSJ9|27c932776e652dab4be9fa9a1cf7337c102656655ce0af40b3defe5ceb9ca594; z_c0=2|1:0|10:1710021254|4:z_c0|92:Mi4xd2o5RVJnQUFBQUFBd05id3BHQkpHQ1lBQUFCZ0FsVk5oaWphWmdDN2dnQUxUQk53RkkyX0FHYmw5em1WeVhNZ3RR|6f0c4552fbaaccf308dc7108b44bd29b974fca6ed28093a9b66f1dd1c76dfeab; q_c1=f1c2262db60448dabcbe1b146d4caa8f|1710021597000|1710021597000; _xsrf=2e087039-846c-4080-8710-a150afdf293c; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1711013966,1711098027,1711180281,1711186079; SESSIONID=kpx1cl4qrM1VO56l6ATbghpsE8HlWxTrkInVlylTJ6u; JOID=U1EdCkw1UW-Bgl_XNzx_s7-a8WEpViAWvuc74kdBFF_Ww2zpWvRVYO-MVtc4e28eyBVIYspLd73rf0rQQZwzIcE=; osd=V1oWA0oxWmSIhFvcPDV5t7SR-GctXSsfuOMw6U5HEFTdymrtUf9cZuuHXd4-f2QVwRNMacFCcbngdEPWRZc4KMc=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1711289957; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1711293062|1711277230'
}


def trans_date(v_timestamp):
    # Convert 10-digit timestamp to time string 10/位时间戳转换为时间字符串
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def tran_gender(gender_tag):
    # Convert gender/性别转换
    if gender_tag == 1:
        return '男'
    elif gender_tag == 0:
        return '女'
    else:  # -1
        return '未知'


def comment_spider(v_result_file, v_answer_list):
    for answer_id in v_answer_list:
        url0 = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset=0&status=open'.format(
            answer_id)
        r0 = requests.get(url0, headers=headers)  # Send request/发送请求
        total = r0.json()['common_counts']  # Total number of comments/一共多少条评论
        print('一共{}条评论'.format(total))
        print('Total {} comments'.format(total))
        # Calculate total pages (20 comments per page)/判断一共多少页（每页20条评论）
        max_page = int(total / 20)
        print('max_page:', max_page)
        # Start crawling loop/开始循环爬取
        for i in range(max_page):
            offset = i * 20
            url = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset={}&status=open'.format(
                answer_id,
                str(offset))
            r = requests.get(url, headers=headers)
            print('正在爬取第{}页'.format(i + 1))
            print('Crawling page {}'.format(i + 1))
            j_data = r.json()
            comments = j_data['data']
            # If there are no comments, end the loop/如果没有评论了，就结束循环
            if not comments:
                print('无评论，退出循环')
                break
            # Otherwise, start crawling/否则开始爬取
            # Define empty lists to store data/定义空列表用于存数据
            answer_urls = []  # 回答url
            authors = []  # 评论作者
            genders = []  # 作者性别
            author_homepages = []  # 作者主页
            author_pics = []  # 作者头像
            create_times = []  # 评论时间
            contents = []  # 评论内容
            child_tag = []  # 评论级别
            vote_counts = []  # 点赞数
            ip_list = []  # IP属地
            for c in comments:  # Root comments/一级评论
                # 回答url
                answer_urls.append('https://www.zhihu.com/answer/' + answer_id)
                # 评论作者
                author = c['author']['member']['name']
                authors.append(author)
                print('作者：', author)
                # 作者性别
                gender_tag = c['author']['member']['gender']
                genders.append(tran_gender(gender_tag))
                # 作者主页
                homepage = 'https://www.zhihu.com/people/' + c['author']['member']['url_token']
                author_homepages.append(homepage)
                # 作者头像
                pic = c['author']['member']['avatar_url']
                author_pics.append(pic)
                # 评论时间
                create_time = trans_date(c['created_time'])
                create_times.append(create_time)
                # 评论内容
                comment = c['content']
                contents.append(comment)
                print('评论内容：', comment)
                # 评论级别
                child_tag.append('一级评论')
                # 点赞数
                vote_counts.append(c['vote_count'])
                # IP属地
                ip_list.append(c['address_text'].replace('IP 属地', ''))
                if c['child_comments']:  # If child comments/如果二级评论存在
                    for child in c['child_comments']:  # 二级评论
                        # 回答url
                        answer_urls.append('https://www.zhihu.com/answer/' + answer_id)
                        # 评论作者
                        print('子评论作者：', child['author']['member']['name'])
                        authors.append(child['author']['member']['name'])
                        # 作者性别
                        genders.append(tran_gender(child['author']['member']['gender']))
                        # 作者主页
                        author_homepages.append(
                            'https://www.zhihu.com/people/' + child['author']['member']['url_token'])
                        # 作者头像
                        author_pics.append(child['author']['member']['avatar_url'])
                        # 评论时间
                        create_times.append(trans_date(child['created_time']))
                        # 评论内容
                        print('子评论内容：', child['content'])
                        contents.append(child['content'])
                        # 评论级别
                        child_tag.append('二级评论')
                        # 点赞数
                        vote_counts.append(child['vote_count'])
                        # IP属地
                        ip_list.append(child['address_text'].replace('IP 属地', ''))
            # 保存数据到csv
            header = True
            if os.path.exists(csv_file):  # 如果csv存在，不写表头，避免重复写入表头
                header = False
            df = pd.DataFrame(
                {
                    '回答url': answer_urls,
                    '页码': [i + 1] * len(answer_urls),
                    '评论作者': authors,
                    '作者性别': genders,
                    '评论内容': contents,
                    '作者主页': author_homepages,
                    '作者头像': author_pics,
                    '评论时间': create_times,
                    '评论级别': child_tag,
                    '点赞数': vote_counts,
                    'IP属地': ip_list,
                }
            )
            # 保存到csv文件
            df.to_csv(v_result_file, mode='a+', index=False, header=header, encoding='utf_8_sig')


if __name__ == '__main__':
    csv_file = '知乎评论.csv'
    # If CSV file exists, delete it first to avoid duplicate data due to appending
    # 如果csv存在，先删除，避免由于追加产生重复数据
    if os.path.exists(csv_file):
        print('文件存在，删除：{}'.format(csv_file))
        os.remove(csv_file)
    # Start crawling, provide related Zhihu popular answer IDs
    # 开始爬取, 相关的知乎热门回答id
    comment_spider(v_result_file=csv_file,  # Save file name/保存文件名
                   v_answer_list=['3442609469', '3442629405', '3442693300', '3442420297', '3442678374', '3442445558', '3442694890', '3442628667', '3442536513', '3442687631', '3442690686', '3442725726', '3442740634', '3442399611', '3443130240', '3442468509', '3442743101', '3442437320', '3442383382', '3442520703', '3442401021', '3442863700', '3443736308', '3442638551', '3442416821', '3442482888', '3442820974', '3442578280', '3442617781', '3442952709', '3442482320', '3443056403'])
    print('抓取完成 退出程序')
    print('Crawling completed. Exiting program')
