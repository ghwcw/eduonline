#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-10
    Project : eduonline
   FileName : adminx.py
Description : 
-------------------------------------------------------------
"""

import xadmin
from apps.course.models import Course, Section, Video, CourseResource


class CourseAdmin():
    list_display = ['id', 'name', 'desc', 'detail', 'courseorg', 'degree', 'learn_time', 'students', 'fav_nums', 'image',
                    'click_nums', 'add_time']
    list_filter = ['id', 'name', 'desc', 'detail', 'courseorg', 'degree', 'learn_time', 'students', 'fav_nums', 'image',
                   'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail']
    model_icon = 'fa fa-heart'

    def save_model(self):
        """保存课程时，统计课程机构的课程数"""
        obj = self.new_obj      # 获取Course对象obj，固定写法
        obj.save()
        if obj.courseorg:
            obj.courseorg.courses = Course.objects.filter(courseorg=obj.courseorg).count()
            obj.courseorg.save()

    data_charts = {
        'students': {
            'title': '学生人数统计图',
            'x-field': 'id',
            'y-field': 'students',
        }
    }


class SectionAdmin():
    list_display = ['id', 'course', 'name', 'add_time']
    list_filter = ['id', 'course', 'name', 'add_time']
    search_fields = ['name']
    model_icon = 'fa fa-navicon'


class VideoAdmin():
    list_display = ['id', 'section', 'name', 'add_time']
    search_fields = ['id', 'section', 'name', 'add_time']
    list_filter = ['name']
    model_icon = 'fa fa-film'


class CourseResourceAdmin():
    list_display = ['id', 'course', 'name', 'add_time', 'download']
    search_fields = ['id', 'course', 'name', 'add_time', 'download']
    list_filter = ['id', 'course', 'name', 'add_time', 'download']
    model_icon = 'fa fa-download'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Section, SectionAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
