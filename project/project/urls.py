"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('set_admin/', views.setRoleAdmin, name='set_admin'),
    path('pregled_predmeta/', views.pregledPredmeta, name='pregled_predmeta'),
    path('dodaj_predmet/', views.dodajPredmet, name='dodaj_predmet'),
    path('details/<int:predmet_id>', views.detaljiPredmeta, name='details'),
    path('edit/<int:predmet_id>', views.urediPredmet, name='edit'),
    path('pocetna/', views.pocetna, name = 'pocetna'),
    path('pregled_profesora/', views.pregledProfesora, name='pregled_profesora'),
    path('dodaj_profesora/', views.dodajProfesora, name="dodaj_profesora"),
    path('details_prof/<int:profesor_id>', views.detaljiProfesor, name='details_prof'),
    path('edit_prof/<int:profesor_id>', views.urediProfesor, name='edit_prof'),
    path('pregled_studenata/', views.pregledStudenata, name='pregled_studenata'),
    path('dodaj_studenta/', views.dodajStudenta, name='dodaj_studenta'),
    path('details_stud/<int:student_id>', views.detaljiStudent, name='details_stud'),
    path('edit_stud/<int:student_id>', views.urediStudent, name='edit_stud'),
    path('upis_predmeta_izvan/<int:student_id>', views.upisPredmeta_izvan, name='upis_predmeta_izvan'),
    path('upis_predmeta_red/<int:student_id>', views.upisPredmeta_red, name='upis_predmeta_red'),
    path('upis_predmeta/<int:predmet_id>', views.upisi_predmet, name='upis_predmeta'),
    path('ispis_predmeta/<int:predmet_id>', views.ispis_iz_predmeta, name='ispis_predmeta'),
    path('popis_studenata/<int:predmet_id>', views.popisStudenataPoPredmetu, name='popis_studenata'),
    path('login_user/', views.loginUser, name = 'login_user'),
    path('logout/', views.logoutUser, name='logout_user'),
    path('izvanredni_stud/', views.pregledStudenata_izvan, name='izvanredni_studenti'),
    path('redovni_stud/', views.pregledStudenata_red, name='redovni_studenti'),
    path('upis_predmeta_izvan_admin/<int:student_id>', views.upisPredmeta_izvan_admin, name='upisni_list_izvan'),
    path('upis_predmeta_red_admin/<int:student_id>', views.upisPredmeta_red_admin, name='upisni_list_red'),
    path('pocetna_prof/', views.pocetnaProfesor, name = 'pocetna_prof'),
    path('pregled_predmeta_prof/', views.pregledPredmetaProf, name='pregled_predmeta_prof'),
    path('popis_studenata_prof/<int:predmet_id>', views.popisStudenataPoPredmetuProf, name='popis_studenata_prof'),
    path('promjena_statusa/<int:predmet_id>', views.promjenaStatusa, name='promjena_statusa'),
    path('status_polozeno/<int:predmet_id>/<int:student_id>/', views.statusPolozi, name='status_polozeno'),
    path('popis_polozenih/<int:predmet_id>', views.popisPolozenih, name='popis_polozenih'),
    path('status_upisan/<int:student_id>/<int:predmet_id>/', views.statusUpisan, name='status_upisan'),
    path('pocetna_stud/', views.pocetna_student, name='pocetna_stud'),
    path('popis_trece/', views.popis_trece, name='treci'),
]
