# coding=utf-8
from datetime import datetime


class ThirdPost(object):
    id = None
    third_id = None
    third_name = None
    post_id = None
    title = None
    author = ""
    tags = ""
    redirect_url = None
    content = ""
    like_num = 0
    comment_num = 0
    read_num = 0
    creatime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_at = None
    can_analysis = 0

    def __init__(self, third_id, third_name, can_analysis):
        self.third_id = third_id
        self.third_name = third_name
        self.can_analysis = can_analysis
