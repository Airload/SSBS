from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from .models import Member
from django.contrib import messages

def member_reg(request):
    if request.method == "GET":
        return render(request, 'users/member_reg.html')
    elif request.method == "POST":
        member_id = request.POST["member_id"]
        passwd = request.POST["passwd"]
        name = request.POST["name"]
        email = request.POST["email"]

        member_id_exists = Member.objects.filter(member_id=member_id).exists()
        email_exists = Member.objects.filter(email=email).exists()

        if member_id_exists:
            messages.error(request, f'{member_id}가 중복됩니다.')
            return render(request, 'users/member_reg.html')
        elif email_exists:
            messages.error(request, f'{email}가 중복됩니다.')
            return render(request, 'users/member_reg.html')
        else:
            Member.objects.create(
                member_id=member_id, passwd=passwd, name=name, email=email, usage_flag='y',
                reg_date=datetime.now(), update_date=datetime.now())
            messages.success(request, f'{name}님 회원가입 되었습니다.')
            return redirect('/pybo/')




def member_login(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    elif request.method == "POST":
        context = {}

        member_id = request.POST.get('member_id')
        passwd = request.POST.get('passwd')

        # 로그인 체크하기
        rs = Member.objects.filter(member_id=member_id, passwd=passwd).first()
        print(member_id + '/' + passwd)
        print(rs)

        #if rs.exists():
        if rs is not None:

            # OK - 로그인
            request.session['m_id'] = member_id
            request.session['m_name'] = rs.name
            return redirect('/pybo/')

        else:

            context['message'] = "로그인 정보가 맞지않습니다.\\n\\n확인하신 후 다시 시도해 주십시오."
            return render(request, 'users/login.html', context)


def member_logout(request):
    request.session.flush()
    return redirect('/pybo/')