# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
import json
import time
import time
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, render_to_response, get_object_or_404, Http404
from django.db.models import Q
from admina.models import Creation2ProjectLabel, Creation, ProjectLabel, Comment, User, Praise, Follow, ProjectUser, \
    Project2ProjectLabel, Project, Recruit
from admina import models


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import uuid
import re, base64

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .Idea_util.ImgVerification import generate_verify_image
from django.views.decorators.csrf import csrf_exempt

# Create your views here.







''' 页面统一功能视图'''


@csrf_exempt
def Check_User_Cookie(req):
    '''
    登陆验证函数，如需登陆，调此函数即可，仍需调试
    @:return 状态值，可通过为true
    @:COOKIE name = User_acconunt
    @:COOKIE name = UUID
    '''
    loginStatus = False
    try:
        user_cookie = req.COOKIES["email"]
        user_uuid_code = req.COOKIES["uuid"]
        try:
            user = models.User.objects.get(Email=user_cookie)
            if user_uuid_code == user_uuid_code:
                loginStatus = True
                return loginStatus
        except:
            return loginStatus
    except:
        return loginStatus


def varidate_char(str, max_length=20):
    '''
    非法字符验证
    :param sql: 
    :param max_length: 
    :return: False  表示字符串中含有非法字符    True 表示字符串中不含有非法字符
    '''
    if len(str) > max_length:
        return False
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@", "!"]
    for char in str:
        if char in dirty_stuff:
            return False
    return True


def varidate_emial(str, max_length=20):
    '''
    邮箱格式验证
    :param str: 
    :param max_length: 
    :return: 
    '''
    if len(str) > max_length:
        return False
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", str) != None:
        return True
    else:
        return False


@csrf_exempt
def get_user_img(req):
    '''
    动态获取用户图片
    :param req: 
    :return: 
    '''
    if req.method == "GET":
        # user = models.User.objects.get(Email='chris156@123.com')
        # img = str(user.Img)
        # print img
        # return HttpResponse('ok')
        return Http404
    elif req.method == "POST":
        result = {
            'status': 0,
            'message': None,
            'img_path': None
        }
        try:
            email = req.COOKIES.get('email')
            print(email)
            username = req.COOKIES.get('username')
            print(username)
        except:
            result['status'] = 0
            result['message'] = '尚未登陆'

            return HttpResponse(json.dumps(result))
        else:
            try:
                user = models.User.objects.get(UserName=username)
            except Exception as e:
                print(e)
                result['status'] = 0
                result['message'] = '获取数据异常'
                return HttpResponse(json.dumps(result))
            else:
                try:
                    result['status'] = 1
                    result['message'] = '路径获取成功'
                    img_path = user.Img.url
                    print(img_path)
                    result['img_path'] = img_path
                except Exception as e:
                    print(e)
                    result['status'] = 1
                    result['message'] = '用户暂未上传图片'
                    img_path = 'photos/2017/09/19/user/default_cdNstvn.jpg'
                    result['img_path'] = img_path
                    return HttpResponse(json.dumps(result))
                else:
                    return HttpResponse(json.dumps(result))


@csrf_exempt
def test(req, param):
    ''''
    测试页面
    '''
    if req.method == "GET":
        teams = models.User.objects.all().filter(Identity=2)

        return render_to_response('team/test.html', {'teams': teams})
    if req.method == "POST":
        data = req.POST["data"]
        return HttpResponse(data)


def index(req):
    '''
    返回首页页面
    :param req: 
    :return: 
    '''
    if req.method == "GET":
        project = models.Project.objects.all()
        label = models.Project2ProjectLabel.objects.all()
        creation = models.Creation.objects.all()
        creationlabel = models.Creation2ProjectLabel.objects.all()
        return render_to_response('idea/index.html',{"projects": project,"labels":label,
                                                     "creations":creation,"creationlabels":creationlabel
                                                     })
    if req.method == "POST":
        pass


@csrf_exempt
def login(req):
    '''
    登陆界面的处理
    :param req: 
    :return: 
    '''
    if req.method == "GET":
        return render_to_response('idea/login.html')
    if req.method == "POST":
        # req.setCharactorEcoding("utf-8")
        result = {}
        result['email'] = None
        result['status'] = None
        result['message'] = ''
        result['username'] = None
        result['uuid'] = None
        try:
            email = req.POST['email']
            password = req.POST['password']
        except Exception as e:
            print(email)
            result['status'] = 0
            result['message'] = '获取信息失败'
            return HttpResponse(json.dumps(result))
        else:
            if varidate_emial(email):
                if models.User.objects.filter(Q(Email=email)):
                    user = models.User.objects.get(Email=email)
                    if user.PassWord == password:
                        user.Uuid = uuid.uuid1()
                        result['status'] = 1
                        result['username'] = user.UserName
                        result['email'] = email
                        req.session['uuid'] = str(user.Uuid)
                        result['message'] = '登陆成功'
                        return HttpResponse(json.dumps(result))
                    elif user.PassWord != password:
                        result['status'] = 0
                        result['message'] = '用户名或密码错误'
                        return HttpResponse(json.dumps(result))
                else:
                    result['status'] = 0
                    result['message'] = '用户名或密码错误'
                    return HttpResponse(json.dumps(result))
            else:
                result['status'] = 0
                result['message'] = '帐号格式不正确'
                message = "message"
                return HttpResponse(json.dumps(result))


@csrf_exempt
def regist(req):
    '''
    注册页面
    :param req: 
    :return: 在客户端留下username 和 email 的cookie 以及uuid session
    '''
    if req.method == 'GET':
        return render_to_response('idea/regist.html')
    if req.method == "POST":
        result = {
            'message': None,
            'status': 0,
            'username': None,
            'emial': None,
            'uuid': None
        }
        try:
            username = req.POST['UserName']
            email = req.POST['Email']
            password = req.POST['Passwd']
        except:
            result['status'] = 0
            result['message'] = '获取信息失败'
            return HttpResponse(json.dumps(result))
        else:
            if not (varidate_char(username) and varidate_emial(email)):
                result['message'] = '输入非法字符'
                result['status'] = 0
                return HttpResponse(json.dumps(result))
            elif models.User.objects.filter(Email=email):
                result['status'] = 0
                result['message'] = '邮箱已经被注册'
                return HttpResponse(json.dumps(result))
            elif models.User.objects.filter(UserName=username):
                result['status'] = 0
                result['message'] = '姓名已被注册'
                return HttpResponse(json.dumps(result))
            else:
                try:
                    models.User.objects.create(Email=email, UserName=username, PassWord=password, Uuid=uuid.uuid1())
                    user = models.User.objects.get(Email=email)
                    user.Img = 'photos/2017/09/19/user/default_cdNstvn.jpg'
                    req.session['uuid'] = str(user.Uuid)
                    result['email'] = email
                    result['username'] = username
                    result['message'] = '注册成功，正在调转'
                    result['status'] = 1
                    return HttpResponse(json.dumps(result))
                except Exception as e:
                    print(e)
                    result['status'] = 0
                    result['message'] = '服务器异常!!'
                    return HttpResponse(json.dumps(result))


@csrf_exempt
def logout(req):
    '''
    注销界面
    :param req: 
    :return: 
    '''
    if req.method == "GET":
        response = render_to_response('idea/Base.html')
        response.delete_cookie('username')
        response.delete_cookie('email')
        return response


def forgetPassword(req):
    '''
    忘记密码页面
    :param req: 
    :return: 
    '''
    if req.method == 'GET':
        stream, strs = generate_verify_image(save_img=False)
        # req.sessions['verifycode'] = strs
        stream = base64.b64encode(stream.getvalue()).encode('ascii')
        req.session['verificode'] = strs
        return render_to_response('idea/forgetPassword.html', {'img': stream})


''' 功能页面相关视图结束'''

''' 团队页面相关视图'''


def team(req):
    '''
    团队页面
    :param req: 
    :return: 
    '''
    if req.method == 'GET':
        ''' 标签查询'''


        sign = req.GET["sign"]
        if sign == "all":
            teams = models.User.objects.filter(Identity=2)
            User2UserLabel = models.User2UserLabel.objects.all()
            labels = models.UserLabel.objects.all()
            return render_to_response('team/team.html', {"teams": teams, "labels": labels,'User2UserLabel': User2UserLabel})
        elif int(sign):
            labels = models.UserLabel.objects.all()
            labels_0 = models.UserLabel.objects.filter(pk=sign)
            # user_2_userLable = models.User2UserLabel.objects.filter(Q(userLabel=labels) & Q(user__Identity=2))
            user_2_userLable = models.User2UserLabel.objects.filter(userLabel=labels_0).filter(user__Identity=2)
            User2UserLabel = models.User2UserLabel.objects.all()
            teams = []
            for obj in user_2_userLable:
                teams.append(obj.user)
            return render_to_response('team/team.html', {"teams": teams, "labels": labels, 'User2UserLabel': User2UserLabel})

    if req.method == 'POST':
        pass

@csrf_exempt
def teamdetails(req, teamid):
    '''
    团队详情页面 所有team 按照创建时间排序
    :param req: 
    :param teamid: 团队ID
    :return: 
    '''
    if req.method == 'GET':
        username = "chris"
        try:
            this_team = models.User.objects.get(Q(pk=teamid) & Q(Identity=2))
            labels = models.User2UserLabel.objects.filter(Q(user__Id=teamid))
            counts = models.Follow.objects.filter(Follower=this_team).count()
            teamcounts = models.Praise.objects.filter(user_prised=this_team).count()
            comments = models.Comment.objects.filter(commited_user_id=teamid).order_by("-Date")
            user = models.User.objects.get(UserName=username)
            comment_id = models.Comment.objects.filter(Q(commited_user_id=teamid) & Q(user=user))
            print (comment_id)
            commentlist = []

            for comment in comments:
                if comment.commentedId is None:
                    newcomment = []
                    newcomment.append(comment)
                    commentlist.append(newcomment)

            for comlist in commentlist:
                for comment in comments:
                    if str(comlist[0].Uuid)==str(comment.commentedId):
                        comlist.append(comment)

        except Exception as e:
            return Http404

        return render_to_response('team/teamdetails.html', {"team": this_team, "labels": labels,"counnt":counts,"comments":commentlist,"teamstar":teamcounts,"id":comment_id})
    if req.method == 'POST':
        content = req.POST["string"]
        username = "chris"
        result = {
            "status": 1,
            "string": None
        }
        try:
            user = models.User.objects.get(UserName=username)
            userteam = models.User.objects.get(Q(Id=teamid) & Q(Identity=2))
        except Exception as e:
            result["status"] = 0
            result["string"] = "空"
            return HttpResponse(json.dumps(result))
        else:
            models.Comment.objects.create(user=user, commited_user=userteam, Content=content)
            return HttpResponse(json.dumps(result))


@csrf_exempt
def teamcomment(req):
    if req.method == 'POST':
        reply_content = req.POST["strings"]
        teamid = req.POST["team_id"]
        commentid = req.POST["comment_id"]
        username = "chris"
        result = {
            "status": 1
        }
        try:
            user = models.User.objects.get(UserName=username)
            userteam = models.User.objects.get(Q(Id=teamid) & Q(Identity=2))
            Comment1 = models.Comment.objects.filter(Id=commentid)
            print Comment1[0].Uuid
        except Exception as e:
            print(e.message)
            result["status"] = 0
            result["string"] = "空"
            return HttpResponse(json.dumps(result))
        else:
            # print(locals())
            models.Comment.objects.create(user=user, commited_user=userteam, Content=reply_content,commentedId=Comment1[0].Uuid)
            return HttpResponse(json.dumps(result))


@csrf_exempt
def teamattend(req):
    '''
    团队详情的关注
    :param req: 
    :return: 
    '''
    if req.method == 'POST':
        try:
            Id = req.POST['Id']
            userId = req.POST['userId']
            FollowUser = Follow.objects.filter(Follower_id=Id, user_id=userId)
            if len(FollowUser) > 0:
                status = 2
            else:
                status = 1
        except Exception as e:
            return HttpResponse('404')
        else:
            return HttpResponse(status)
    if req.method == 'GET':
        pass


@csrf_exempt
def teamattend1(req):
    '''
    团队详情的点赞
    :param req: 
    :return: 
    '''
    if req.method == 'POST':
        try:
            Id = req.POST['Id']
            userId = req.POST['userId']
            praiseUser = Praise.objects.filter(user_prised_id=Id, user_id=userId)
            if len(praiseUser) > 0:
                status = 2
            else:
                status = 1
        except Exception as e:
            return HttpResponse('404')
        else:
            return HttpResponse(status)
    if req.method == 'GET':
        pass

def teamhelpapplication(req, teamhelpid):
    '''
    团队帮助申请
    :param req: 
    :param teamhelpid: 
    :return: 
    '''
    if req.method == 'GET':
        try:
            teamhelp = models.User.objects.get(Id=teamhelpid)
        except:
            return HttpResponse('404')
        else:
            if int(teamhelp.Identity) == 2:
                return render_to_response('team/teamhelpapplication.html', {'teamhelp': teamhelp})
            else:
                return HttpResponse('404')
    if req.method == 'POST':
        pass


def service(req):
    '''
    服务页面
    :param req:
    :return:
    '''
    if req.method == 'GET':
        return render_to_response('idea/service.html')
    if req.method == "POST":
        pass


def ordinance(req):
    '''
    隐私条例页面详情
    :param req:
    :return:
    '''
    if req.method == 'GET':
        return render_to_response('idea/ordinance.html')
    if req.method == "POST":
        pass


''' 团队页面相关视图结束  '''

''' 创意灵感 页面相关部分开始'''


def crdetails(req):
    '''
    创意详情
    :param req: 
    :return: 
    '''
    if req.method == 'GET':
        creationId = req.GET['creationId']
        creation = Creation.objects.get(Id=creationId)
        labels = Creation2ProjectLabel.objects.filter(creation_id=creationId)
        comments = Comment.objects.filter(creation_id = creationId).order_by("-Date")



        commentlist = []

        for comment in comments:    #将所有的第一条回复添加进来 结果:[[head],[head]]
            if comment.commentedId is None:
                newcomment = []   
                newcomment.append(comment)
                commentlist.append(newcomment) #    [[head],[head],[head],[head]]


        for comlist in commentlist:    # 对每个列表循环  结果: [ [head,hui,hui],[head,hui,hui],[head] ]
            for comment in comments:
                if str(comlist[0].Uuid)==str(comment.commentedId):
                    comlist.append(comment)   
                       #   [[head,hui,hui],[head,hui,hui ],[head],[head]]


        alllables = []  # 找出本创意所有的标签
        for label in labels:
            alllables.append(label.projectLabel.Id)
        alllables = list(set(alllables))

        creation2crojectLabels = Creation2ProjectLabel.objects.filter(projectLabel_id__in = alllables)    #所有相关标签的 所有的 标签2项目
        return render_to_response('creation/crdetails.html',{"creation":creation,"comments":commentlist,"creation2crojectLabels":creation2crojectLabels[:2],"labels":labels[:3]})

    if req.method == "POST":
        pass


@csrf_exempt
def creations(req):
    '''
    创意灵感一级二级页面项目显示  
    '''
    
    # userId = int(req.COOKIES.get('user'))
    userId = 3
    try:
        if req.method == 'GET':
            sign = req.GET['sign']
            # 如果是所有项目
            if sign == "all":
                creations = Creation.objects.all().order_by("Date")
            # 如果有特殊标签
            else:
                CreationLabelObjs = Creation2ProjectLabel.objects.filter(projectLabel=sign)
                creations = []
                for obj in CreationLabelObjs:
                    creations.append(obj.creation)

            projectLabels = ProjectLabel.objects.all()
            praises = Praise.objects.all()
            follows = Follow.objects.all()

            return render_to_response('creation/index.html',
                                      {'creations': creations, 'projectLabels': projectLabels, 'userId': userId,
                                       'follows': follows, 'praises': praises})
    except Exception as e:
        print(e)
        return HttpResponse("<script type='text/javascript'>alert('数据有异常，请稍后再试')</script>")





@csrf_exempt
def attend(req):
    '''
    Id的关注类型
    1为被关注创意
    2为被关注项目
    3为被关注用户

    status
    状态值：0为操作失败，1为关注成功，2 为取消关注成功
    '''
    status = 0
    try:
        Id = req.POST['Id']
        userId = req.POST['userId']
        attendType = int(req.POST['attendType'])

        if attendType == 1:
            FollowCreation = Follow.objects.filter(creation_id = Id, user_id = userId)
            if len(FollowCreation) > 0:
                FollowCreation.delete()
                status = 2
            else:
                Follow.objects.create(creation_id=Id, user_id=userId)
                status = 1
                
        elif attendType == 2:
            FollowProject = Follow.objects.filter(project_id = Id, user_id = userId)
            if len(FollowProject) > 0:
                FollowProject.delete()
                status = 2
            else:
                Follow.objects.create(project_id=Id, user_id=userId)
                status = 1

        elif attendType == 3:
            FollowUser = Follow.objects.filter(Follower_id = Id, user_id = userId)
            if len(FollowUser) > 0:
                FollowUser.delete()
                status = 2
            else:
                Follow.objects.create(Follower_id=Id, user_id=userId)
                status = 1
        return HttpResponse(status)
    except:
        return HttpResponse(status)





@csrf_exempt
def star(req):
    '''
    点赞
    1为创意
    2为项目
    3为个人/团队

    status
    状态值：0为失败，1为成功， 2为取消点赞成功
    '''
    status = 0
    try:
        Id = req.POST["Id"]
        userId = req.POST["userId"]
        starType = int(req.POST["starType"])
        if starType == 1:    #如果是创意
            try:
                p = Praise.objects.get(creation_id=Id, user_id=userId).delete()    #尝试取消点赞
                status = 2
            except:
                p = Praise.objects.create(creation_id=Id, user_id=userId)
                status = 1
            return HttpResponse(status)
        elif starType ==2:
            try:
                p = Praise.objects.get(project_id=Id, user_id=userId).delete()
                status = 2
            except:
                p = Praise.objects.create(project_id=Id, user_id=userId)
                status = 1

            return HttpResponse(status)
        elif starType ==3:
            PraiseUser = Praise.objects.filter(user_prised_id=Id, user_id=userId)
            if len(PraiseUser) > 0:
                PraiseUser.delete()
                status = 2
            else:
                Praise.objects.create(user_prised_id=Id, user_id=userId)
                status = 1
            # try:
            #     PraiseUser = Praise.objects.get(user_prised_id=Id, user_id=userId).delete()
            #     status = 2
            # except:
            #     PraiseUser = Praise.objects.create(user_prised_id=Id, user_id=userId)
            #     status = 1
        return HttpResponse(status)
    except Exception as e:
        print(e)
        return HttpResponse(status)

@csrf_exempt
def comment(req):
    '''
    创意评论
    :param req:
    :return:
    '''
    status = 0
    if req.method =='POST':
        try:
            username = "chris"
            creationId = req.POST["creationId"]
            content = req.POST["content"]
            user = models.User.objects.get(UserName=username)
            creation = models.Creation.objects.get(pk = creationId)
            models.Comment.objects.create(user = user ,creation = creation , Content = content)
            status = 1
            return HttpResponse(status)


        except Exception as e:
            print(e)
            return HttpResponse(status)

    if req.method =='GET':
        content = "hello world"
        username = "chris"
        creationid = 3
        user = models.User.objects.get("UserName=username")
        creation = models.Creation.objects.get(pk=creationid)
        models.Comment.objects.create(user=user, creation=creation, Content=content)
        return HttpResponse("TRUE")
''' 创意灵感 页面相关部分结束'''

''' 招募项目 相关页面开始'''


def apply(req):
    '''
    招募项目申请表
    '''
    if req.method == 'GET':
        return render_to_response('project/apply.html')
    if req.method == 'POST':
        pass


'''

提出建议页面详情
'''


def advice(req):
    if req.method == 'GET':
        return render_to_response('idea/advice.html')
    if req.method == "POST":
        pass


'''

招募项目详情
'''


def redetails(req):
    '''
        招募项目详情
        :param req:
        :return:
    '''
    if req.method == 'GET':
        projectId = req.GET['projectId']
        project = Project.objects.get(Id=projectId)
        labels = Project2ProjectLabel.objects.filter(project_id=projectId)
        praises = Praise.objects.all()
        follows = Follow.objects.all()
        comments = Comment.objects.filter(project_id=projectId).order_by("-Date")


        commentlist = []

        for comment in comments:
            if comment.commentedId is None:
                newcomment = []
                newcomment.append(comment)
                commentlist.append(newcomment)

        for comlist in commentlist:
            for comment in comments:
                if str(comlist[0].Uuid) == str(comment.commentedId):
                    comlist.append(comment)
        alllables = []  # 找出本创意所有的标签
        for label in labels:
            alllables.append(label.projectLabel.Id)
        alllables = list(set(alllables))
        project2projectLabel = Project2ProjectLabel.objects.filter(projectLabel_id__in=alllables)  # 所有相关标签的 所有标签2项目
        recruit = models.Recruit.objects.filter(project__Id=projectId)
        if recruit.exists():
            recruit = recruit[0]
        a = recruit.EndTime.strftime("%Y-%m-%d %H:%M:%S")
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))


        return render_to_response('project/redetails.html',{"project": project, "project2projectLabels": project2projectLabel[:2],
                                   "labels": labels[:3], "recruit": recruit, "EndTime": timeStamp,'follows': follows,'praises': praises,"comment":commentlist,})


    if req.method == "POST":
         pass

@csrf_exempt
def project_comment(req):
    '''
    项目评论
    :param req:
    :return:
    '''


    status = 0
    if req.method == 'POST':
        try:
            username = "chris"
            projectId = req.POST["projectId"]
            content = req.POST["content"]
            user = models.User.objects.get(UserName=username)
            project = models.Project.objects.get(pk=projectId)
            models.Comment.objects.create(user=user, project=project, Content=content)
            status = 1
            return HttpResponse(status)


        except Exception as e:
            print(e)
            return HttpResponse(status)
        if req.method == 'GET':
            content = "hello world"
            username = "chris"
            projectid = 3
            user = models.User.objects.get("UserName=username")
            peoject = model.Project.objects.get(pk=projectid)
            models.Comment.objects.create(user=user, project=project, Content=content)
            return HttpResponse("TRUE")

@csrf_exempt
def recruit_apply(req):
    '''
       招募项目申请
    '''

    status = 0
    if req.method == 'POST':
        try:
            username = "chris"
            projectId = req.POST["projectId"]
            content = req.POST["describe"]
            user = models.User.objects.get(UserName=username)
            recruit = models.Recruit.objects.get(project=projectId)
            models.Apply.objects.create(user=user, recruit=recruit, Describe=content)
            status = 1
            return HttpResponse(status)
        except Exception as e:
            print(e.message)

        finally:
            return HttpResponse(status)




@csrf_exempt
def projects(req):
    '''
    招募项目一级二级页面项目显示
    '''
    try:
        if req.method == 'GET':
            sign = req.GET['sign']
            #  如果是所有项目
            if sign == "all":
                projects = Project.objects.all().order_by("StartTime")
            else:
                projects = []
                ProjectLabelObjs = Project2ProjectLabel.objects.filter(projectLabel=sign)
                for obj in ProjectLabelObjs:
                    projects.append(obj.project)
            #################
            recruit_all = []
            for project in projects:
                recruit = models.Recruit.objects.filter(project__Id=project.Id)
                recruit_all.append(recruit)

            all_recruit = zip(projects, recruit_all)
            return render_to_response('project/recruit.html', {'projectLabels': ProjectLabel.objects.all(), "all_recruit": all_recruit})
        else:
            id = req.POST['projectId']
            project = get_object_or_404(Project, pk=id)
            comments = Comment.objects.fitler(project=id).order_by('Date')
            return render_to_response('project/recruit.html',
                                      {'comments': comments})
    except Exception as e:
        print(e)
        return HttpResponse("<script type='text/javascript'>alert('数据有异常，请稍后再试')</script>")
''' 招募项目相关页面结束'''

''' 开发项目相关页面开始'''

@csrf_exempt
def deprojects(req):
    '''
    开发项目一级页面项目显示
    '''
    try:
        if req.method == 'GET':
            sign = req.GET['sign']
            #  如果是所有项目
            if sign == "all":
                projects = Project.objects.filter(Q(Statue=3)|Q(Statue=5)).order_by("StartTime")
            else:
                projects = []
                ProjectLabelObjs = Project2ProjectLabel.objects.filter(projectLabel=sign)
                for obj in ProjectLabelObjs:
                    projects.append(obj.project)
            return render_to_response('project/deprojects.html', {'projectLabels': ProjectLabel.objects.all(), "projects": projects})
        else:
            id = req.POST['projectId']
            project = get_object_or_404(Project, pk=id)
            comments = Comment.objects.fitler(project=id).order_by('Date')
            return render_to_response('project/deprojects.html',
                                      {'comments': comments})
    except Exception as e:
        print(e)
        return HttpResponse("<script type='text/javascript'>alert('数据有异常，请稍后再试')</script>")
    if req.method == 'POST':
        pass

@csrf_exempt
def dedetails(req):
    '''
    开发项目二级页面详情
    '''
    if req.method == 'GET':
        projectId = req.GET['projectId']
        project = Project.objects.get(Id=projectId)
        labels = Project2ProjectLabel.objects.filter(project_id=projectId)
        praises = Praise.objects.all()
        follows = Follow.objects.all()
        comments = Comment.objects.filter(project_id=projectId).order_by("-Date")

        alllables = []  # 找出本项目所有的标签
        for label in labels:
            alllables.append(label.projectLabel.Id)
            alllables = list(set(alllables))
        return render_to_response('project/dedetails.html',{"project":project,"labels": labels[:3],})
    if req.method == 'POST':
        pass


''' 开发项目相关页面结束'''



'''个人中心相关页面'''


def homepage(req):
    if req.method == 'GET':
        return render_to_response('personal/homepage.html')
    if req.method == 'POST':
        pass


def release(req):
    '''
    发布项目页面
    :param req:
    :return:
    '''
    if req.method == 'GET':
        obj = models.ProjectLabel.objects.all()
        return render_to_response('personal/release.html', {"labels": obj})
    if req.method == "POST":
        pass


def editprofile(req):
    if req.method == 'GET':
        return render_to_response('personal/editprofile.html')
    if req.method == 'POST':
        pass



'''个人中心相关页面结束'''

