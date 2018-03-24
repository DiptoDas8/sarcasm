from __future__ import print_function

import facebook
import xlwt
from pprint import pprint

def data_collection():
    '''make a list of facebook pages where sarcasm containing posts can be found'''
    pages = ['sarcasmLOL', 'SarcasmMother']

    '''get a valid token, try to get a longer lasting one'''
    graph = facebook.GraphAPI(
        access_token="EAACEdEose0cBAJisENplwbIdhxkjt1jdHq57xHu6oYZCmf28lYmED15ZAHl7NDtWNs76nZCxq3KZBpBIYxw35AR10qZCSLinByZA728LAET7CpqByYzoj3CvWqtZBepF4NaX0cI310gwZALMzPMVPQoS8mjNtYnT2GkSr1Fcy6dQmvsUAJYxaMoHjovbmBKhKeeBHWVJY6TPCbXCxj9kBpPK",
        version="2.7")

    '''create an excel file and allot one sheet for each page'''
    book = xlwt.Workbook()
    for pg in range(len(pages)):
        ''' len(pages) '''
        page_name = pages[pg]
        sheet = book.add_sheet(page_name)
        '''
            a:         b: 
            c: caption,created_time,comments    #
            d: description                      #
            e: 
            f: full_picture                     #
            g:         h: 
            i: id (post_id)                     #
            j:         k: 
            l: link                             #
            m: message,message_tags             #
            n: name                             #
            o: 
            p: place                            #
            q: 
            r: reactions (like, love, haha, wow, sad, angry)    #
            s: source,story          #
            t: type, timeline_visibility        #
            u: updated_time                     #
            v:         w:         x:         y:         z:
        '''
        columns = ['post_id', 'name', 'message', 'message_tags', 'caption', 'description', 'story', 'comments',
                   'like', 'love', 'haha', 'wow', 'sad', 'angry', 'full_picture', 'place', 'type', 'source', 'link',
                   'timeline_visibility', 'created_time', 'updated_time']
        for index, col_header in enumerate(columns):
            sheet.row(0).write(index, col_header)
        page = graph.get_object(id=page_name)

        single_page_id = page['id']
        page_newsfeed = graph.get_object(id=single_page_id, fields='feed')
        page_newsfeed_data = page_newsfeed['feed']['data']
        # pprint(page_newsfeed_data)
        for p in range(len(page_newsfeed_data)):
            '''len(page_newsfeed_data)'''
            single_post_id = page_newsfeed_data[p]['id']
            # print()
            # pprint(single_post_id)
            single_post = graph.get_object(id=single_post_id, fields='id, name, message, message_tags, caption, description,\
                                                        story, comments,\
                                                        reactions.type(LIKE).limit(0).summary(1).as(like),\
                                                        reactions.type(LOVE).limit(0).summary(1).as(love),\
                                                        reactions.type(HAHA).limit(0).summary(1).as(haha),\
                                                        reactions.type(WOW).limit(0).summary(1).as(wow),\
                                                        reactions.type(SAD).limit(0).summary(1).as(sad),\
                                                        reactions.type(ANGRY).limit(0).summary(1).as(angry),\
                                                        full_picture, place, type, source, link,\
                                                        timeline_visibility, created_time, updated_time')
            # pprint(single_post)
            # print(single_post.keys())

            '''create row for each post'''
            row = sheet.row(p + 1)
            for index, col_header in enumerate(columns):
                if col_header not in single_post.keys():
                    if col_header == 'post_id':
                        value = single_post_id
                    else:
                        # print('misssing value: %s'%(col_header))
                        ''' missing data '''
                        value = '***'
                elif col_header in ['like', 'love', 'haha', 'wow', 'sad', 'angry']:
                    count = single_post[col_header]['summary']['total_count']
                    # print('reaction found %s %d'%(col_header, count))
                    value = count
                elif col_header == 'comments':
                    # print('comments')
                    value = 'column_placeholder'
                else:
                    value = single_post[col_header]

                # print(col_header, value)
                row.write(index, value)

    book.save("book.xls")

data_collection()
