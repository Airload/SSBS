from django.urls import path,include

from.import views

urlpatterns = [
    path('',views.index, name='report'),
    path('goun/',views.goun, name='goun'),
    path('gemnam/',views.gemnam, name='gemnam'),
    path('dajeung/',views.dajeung, name='dajeung'),
    path('depyeung/',views.depyeung, name='depyeung'),
    path('dodam/',views.dodam, name='dodam'),
    path('boram/',views.boram, name='boram'),
    path('bugang/',views.bugang, name='bugang'),
    path('serom/',views.serom, name='serom'),
    path('sodam/',views.sodam, name='sodam'),
    path('sojeung/',views.sojeung, name='sojeung'),
    path('areum/',views.areum, name='areum'),
    path('yeongi/',views.yeongi, name='yeongi'),
    path('yeondong/',views.yeondong, name='yeondong'),
    path('yeonseo/',views.yeonseo, name='yeonseo'),
    path('janggun/',views.janggun, name='janggun'),
    path('jeondong/',views.jeondong, name='jeondong'),
    path('jeonui/',views.jeonui, name='jeonui'),
    path('jochiwon/',views.jochiwon, name='jochiwon'),
    path('jongchong/',views.jongchong, name='jongchong'),
    path('hansol/',views.hansol, name='hansol'),

]

