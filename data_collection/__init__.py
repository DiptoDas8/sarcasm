from __future__ import print_function

import facebook
import requests
import xlwt
from pprint import pprint

def data_collection():
    '''make a list of facebook pages where sarcasm containing posts can be found'''
    pages = ['sarcasmLOL', 'SarcasmMother']

    '''get a valid token, try to get a longer lasting one'''
    graph = facebook.GraphAPI(
        access_token="EAACEdEose0cBAA7ZArUZA3XgTsHrnj3foZAVZAk8Oi7WpGwLkSoqmlqkgODDn7b0Do5k66UrpZBGFb1AWPFTIZAVarZBV7cUV73Q5O3DtyQdlfuKAEDRwclvDU4UukeiASvmseYLmt6Dram9idgKgilI54kXI6X5td2xXCnBhg8tf89PbMZB5asmdhP4I9iYZAJj1VB4weAZA6W5b5ZAjmEN324",
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
            m: message             #
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
        columns = ['post_id', 'name', 'message', 'caption', 'description', 'story', 'comments',
                   'like', 'love', 'haha', 'wow', 'sad', 'angry', 'full_picture', 'place', 'type', 'source', 'link',
                   'timeline_visibility', 'created_time', 'updated_time']
        for index, col_header in enumerate(columns):
            sheet.row(0).write(index, col_header)
        page = graph.get_object(id=page_name)

        single_page_id = page['id']
        big_page_newsfeed = {'data':[]}
        # page_newsfeed = graph.get_object(id=single_page_id, fields='feed')
        page_newsfeed = graph.get_connections(single_page_id, 'feed')
        while(True):
            try:
                # pprint(page_newsfeed)
                big_page_newsfeed['data'] = big_page_newsfeed['data'] + page_newsfeed['data']
                # Attempt to make a request to the next page of data, if it exists.
                page_newsfeed = requests.get(page_newsfeed['paging']['next']).json()
            except KeyError:
                # When there are no more pages (['paging']['next']), break from the
                # loop and end the script.
                break
        # pprint (big_page_newsfeed)

        page_newsfeed_data = big_page_newsfeed['data']
        # page_newsfeed_data = page_newsfeed['feed']['data']
        # pprint(page_newsfeed_data)
        for p in range(len(page_newsfeed_data)):   #
            '''len(page_newsfeed_data)'''
            single_post_id = page_newsfeed_data[p]['id']
            # print()
            # pprint(single_post_id)
            single_post = graph.get_object(id=single_post_id, fields='id, name, message, caption, description,\
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
            # print('hi')

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
                try:
                    row.write(index, value)
                except Exception as e:
                    pprint(single_post)
                    print(e)
            #     print('hi2')
            # print('hi3')

    book.save("book.xls")

data_collection()
