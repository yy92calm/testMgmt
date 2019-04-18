# -*- coding: utf-8 -*-  
from django.db import models

class Project(models.Model):
    prj_id = models.AutoField(primary_key=True, null=False)
    prj_num = models.CharField(max_length=50,null=True, blank=True,verbose_name=u'JIRA单号')
    prj_name = models.CharField(max_length=50,null=True, blank=True,verbose_name=u'JIRA单名')
    description = models.CharField(max_length=100,null=True, blank=True,verbose_name=u'当前状态')
    begin_time = models.TextField(max_length=50,null=True, blank=True,verbose_name=u'提测时间')
    end_time = models.TextField(max_length=50,null=True, blank=True,verbose_name=u'上线时间')
    QC = models.CharField(max_length=100,null=True, blank=True,verbose_name=u'跟进人')

    def __str__(self):
        return self.prj_name

class Case(models.Model):
    case_id = models.AutoField(primary_key=True, null=False)
    case_locate = models.TextField(null=True, blank=True,verbose_name=u'模块')
    case_sort = models.IntegerField(null=True, blank=True,verbose_name=u'顺序')
    case_name = models.CharField(max_length=100,verbose_name=u'用例标题')
    case_pre = models.TextField(null=True, blank=True,verbose_name=u'前置条件')
    case_type = models.CharField(max_length=50,null=True, blank=True,verbose_name=u'测试类型')
    case_func = models.TextField(null=True, blank=True,verbose_name=u'操作步骤')
    case_expect = models.TextField(null=True, blank=True,verbose_name=u'期望结果')
    case_result = models.CharField(max_length=50,null=True, blank=True,verbose_name=u'测试结果')
    case_level = models.CharField(max_length=50,null=True, blank=True,verbose_name=u'优先级')
    case_creator = models.CharField(max_length=50, null=True, blank=True,verbose_name=u'设计人')
    case_executor = models.CharField(max_length=50, null=True, blank=True,verbose_name=u'执行人')
    case_time = models.CharField(max_length=50,null=True, blank=True,verbose_name=u'执行时间')
    case_content = models.TextField(null=True, blank=True,verbose_name=u'备注')
    project = models.ForeignKey('Project', to_field="prj_id", null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.case_name

class Merge(models.Model):
    cell_range = models.TextField(null=True, blank=True,verbose_name=u'合并区域')
    project = models.ForeignKey('Project', to_field="prj_id", null=True, blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.cell_range