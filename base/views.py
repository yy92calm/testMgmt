#coding:utf-8
from django.shortcuts import render
from django.template import Template
from base.models import Project, Case, Merge
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.core import serializers
import time
import json
import numpy as np
from xlwt import *
import os
from StringIO import StringIO

# Create your views here.

# 项目查询
def project_index(request):
    prj_list = Project.objects.all()
    return render(request, "base/project/index.html", {"prj_list": prj_list})

# 项目增加
def project_add(request):
    if request.method == 'POST':
        prj_num = request.POST['prj_num']
        prj_name = request.POST['prj_name']
        description = request.POST['description']
        begin_time = request.POST['begin_time']
        end_time = request.POST['end_time']
        QC = request.POST['QC']
        project = Project(prj_num=prj_num,prj_name=prj_name,description=description,begin_time=begin_time,end_time=end_time,QC=QC)
        project.save()
        return HttpResponseRedirect("/base/project/")
    return render(request, "base/project/add.html")

# 项目修改
def project_update(request):
    if request.method == 'POST':
        prj_id = request.POST['prj_id']
        prj_num = request.POST['prj_num']
        prj_name = request.POST['prj_name']
        description = request.POST['description']
        begin_time = request.POST['begin_time']
        end_time = request.POST['end_time']
        QC = request.POST['QC']
        Project.objects.filter(prj_id=prj_id).update(prj_num=prj_num,prj_name=prj_name,description=description,begin_time=begin_time,end_time=end_time,QC=QC)
        return HttpResponseRedirect("/base/project/")
    prj_id = request.GET['prj_id']
    project = Project.objects.get(prj_id=prj_id)
    return render(request, "base/project/update.html", {"project": project})

# 项目删除
def project_delete(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        Project.objects.filter(prj_id=prj_id).delete()
        return HttpResponseRedirect("base/project/")

# 用例查询
def case_index(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        case_list =[]
        merge_list = []
        raw_case_list = json.loads(serializers.serialize('json',Case.objects.filter(project=prj_id).order_by('case_sort')))
        raw_projects = json.loads(serializers.serialize('json',Project.objects.filter(prj_id=prj_id)))
        raw_merge_list = json.loads(serializers.serialize('json',Merge.objects.filter(project=prj_id)))
        for raw_case in raw_case_list:
            raw_case_dict=raw_case[u'fields'].copy()
            raw_case_dict.update({'case_id':raw_case[u'pk']})
            case_list.append(raw_case_dict)
        for raw_merge in raw_merge_list:
            raw_merge_dict = raw_merge[u'fields'].copy()
            merge_list.append(raw_merge_dict)

        project = raw_projects[0][u'fields']
        return render(request, "base/case/index.html", context=({"case_list":json.dumps(case_list),"project":json.dumps(project),"merge_list":json.dumps(merge_list),'prj_id':prj_id}))

def case_export(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        #导出excel表格
        list_obj = Case.objects.filter(project=prj_id).order_by('case_sort')
        raw_projects = json.loads(serializers.serialize('json',Project.objects.filter(prj_id=prj_id)))
        project = raw_projects[0][u'fields']
        if list_obj:
            # 创建工作薄
            ws = Workbook(encoding='utf-8')
            w = ws.add_sheet(u'%s' % (project[u'prj_num']))
            w.write(0, 0, u"序号")
            w.write(0, 1, u"模块")
            w.write(0, 2, u"用例标题")
            w.write(0, 3, u"前置条件")
            w.write(0, 4, u"测试类型")
            w.write(0, 5, u"操作步骤")
            w.write(0, 6, u"期望结果")
            w.write(0, 7, u"测试结果")
            w.write(0, 8, u"优先级")
            w.write(0, 9, u"设计人")
            w.write(0, 10, u"执行人")
            w.write(0, 11, u"执行时间")
            w.write(0, 12, u"备注")
            # 写入数据
            excel_row = 1
            for obj in list_obj:
                data_sort = obj.case_sort
                data_locate = obj.case_locate
                data_name = obj.case_name
                data_pre = obj.case_pre
                data_type = obj.case_type
                data_func = obj.case_func
                data_expect = obj.case_expect
                data_result = obj.case_result
                data_level = obj.case_level
                data_creator = obj.case_creator
                data_executor = obj.case_executor
                data_time = obj.case_time
                data_content = obj.case_content

                w.write(excel_row, 0, data_sort)
                w.write(excel_row, 1, data_locate)
                w.write(excel_row, 2, data_name)
                w.write(excel_row, 3, data_pre)
                w.write(excel_row, 4, data_type)
                w.write(excel_row, 5, data_func)
                w.write(excel_row, 6, data_expect)
                w.write(excel_row, 7, data_result)
                w.write(excel_row, 8, data_level)
                w.write(excel_row, 9, data_creator)
                w.write(excel_row, 10, data_executor)
                w.write(excel_row, 11, data_time)
                w.write(excel_row, 12, data_content)
                excel_row += 1
            # 检测文件是够存在
            # 方框中代码是保存本地文件使用，如不需要请删除该代码
            ###########################
            exist_file = os.path.exists("excel/%s.xls" % (project[u'prj_num']))
            if exist_file:
                os.remove(r"excel/%s.xls" % (project[u'prj_num']))
            ws.save("excel/%s.xls" % (project[u'prj_num']))
            ############################
            sio = StringIO()
            ws.save(sio)
            sio.seek(0)
            response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xls' % (project[u'prj_num'])
            response.write(sio.getvalue())
            return response

# xmind形式用例
def case_xmind(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        raw_case_list = json.loads(serializers.serialize('json',Case.objects.filter(project=prj_id).order_by('case_sort')))
        raw_projects = json.loads(serializers.serialize('json',Project.objects.filter(prj_id=prj_id)))
        mind = {"meta":{"name":"case","author":"yy92calm","version":"0.2"},"format":"node_array"}
        
        data = []
        temp_root={}
        parent_node = u""
        project = raw_projects[0][u'fields']
        temp_root['id'] = "root"
        temp_root['isroot'] = True
        temp_root['topic'] = "单号：%s\n主题：%s\n测试人员：%s" % (project[u'prj_num'],project[u'prj_name'],project[u'QC'])
        data.append(temp_root)
        for raw_case in raw_case_list:
            locate_node = {}
            name_node = {}
            pre_node = {}
            func_node = {}
            expect_node = {}
            temp_case = raw_case[u'fields']
            if temp_case[u'case_locate'] == u"":
                pass
            else:
                parent_node = "%d" % temp_case[u'case_sort']
                locate_node[u'id']="%d" % temp_case[u'case_sort']
                locate_node[u'parentid']=u"root"
                locate_node[u'topic'] = temp_case[u'case_locate']
                locate_node[u'direction']=u"right"
                data.append(locate_node)
            
            #用例名称
            name_node[u'id']="%d_name" % temp_case[u'case_sort']
            name_node[u'parentid']=parent_node
            name_node[u'topic'] = temp_case[u'case_name']
            name_node[u'direction']=u"right"
            #name_node[u'expanded']=False
            
            #前置条件
            #pre_node[u'id']="%d_pre" % temp_case[u'case_sort']
            #pre_node[u'parentid'] = name_node[u'id']
            #pre_node[u'topic'] = temp_case[u'case_pre']
            #pre_node[u'direction']=u"right"
            #pre_node[u'expanded']=False

            #操作步骤
            #func_node[u'id']="%d_func" % temp_case[u'case_sort']
            #func_node[u'parentid'] = pre_node[u'id']
            #func_node[u'topic'] = temp_case[u'case_func']
            #func_node[u'direction']=u"right"
            #func_node[u'expanded']=False
      
            #期望结果
            expect_node[u'id']="%d_expect" % temp_case[u'case_sort']
            expect_node[u'parentid'] = name_node[u'id']
            expect_node[u'topic'] = temp_case[u'case_expect']
            expect_node[u'direction']=u"right"
            #expect_node[u'expanded']=False
            
            data.append(name_node)
            #data.append(pre_node)
            #data.append(func_node)
            data.append(expect_node)
        
        mind[u'data']=data
        return render(request, "base/case/freemind.html",{"mind_list":json.dumps(mind)})

# 用例修改
def case_update(request):
    if request.method == 'POST':
        raw_data = request.POST.getlist('excelData')
        prj_id = request.POST.getlist('prj_id')
        raw_delete = request.POST.getlist('deleteList')
        raw_merge = request.POST.getlist('mergeList')
        raw_unmerge = request.POST.getlist('unmergeList')
        for data in raw_data:
            case_list = data.split(",")
            if case_list[13]==u'':
                case = Case(case_sort=int(case_list[0]),case_locate=case_list[1],case_name=case_list[2],case_pre=case_list[3],case_type=case_list[4],case_func=case_list[5],case_expect=case_list[6],case_result=case_list[7],case_level=case_list[8],case_creator=case_list[9],case_executor=case_list[10],case_time=case_list[11],case_content=case_list[12],project_id=int(prj_id[0]))
                case.save()
            else:
                Case.objects.filter(case_id=int(case_list[13])).update(case_sort=int(case_list[0]),case_locate=case_list[1],case_name=case_list[2],case_pre=case_list[3],case_type=case_list[4],case_func=case_list[5],case_expect=case_list[6],case_result=case_list[7],case_level=case_list[8],case_creator=case_list[9],case_executor=case_list[10],case_time=case_list[11],case_content=case_list[12],project_id=int(prj_id[0]))
        #Case.objects.filter(case_id=case_id).update(case_name=case_name,case_pre=case_pre,case_type=case_type,case_func=case_func,case_expect=case_expect,case_result=case_result,case_level=case_level,case_creator=case_creator,case_executor=case_executor,case_time=case_time,case_content=case_content)
        if len(raw_delete)>0:
            for item in raw_delete:
                delete_list = item.split(",")
                if delete_list[13]==u'':
                    pass
                else:
                    Case.objects.filter(case_id=int(delete_list[13])).delete()
        
        if len(raw_merge)>0:
            for temp_merge in json.loads(raw_merge[0]):
                merge = Merge(cell_range=temp_merge,project_id=int(prj_id[0]))
                merge.save()
        
        if len(raw_unmerge)>0:
            for temp_unmerge in json.loads(raw_unmerge[0]):
                Merge.objects.filter(project_id=int(prj_id[0])).filter(cell_range=temp_unmerge).delete()

        return HttpResponseRedirect(("/base/case/?prj_id=%s") % prj_id[0])

def emailList(request):
    return render(request, "base/reports/email.html")