from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Predmeti, Nositelj, Role, Status, UpisniList
from .forms import PredmetiForm, RoleForm, StatusForm, NositeljForm, UserForm, UpisniListForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.db.models import Count, Sum, Min, Max, Avg
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from .decorators import admin_required, profesor_required, student_required
# Create your views here.

#postavljanje glavnog admina kao rolu admina(koristi se samo jednom)
# def setRoleAdmin(request):
#   if request.method == 'GET':
#     adminForm = RoleForm()
#     return render(request, 'set_admin.html', {'form': adminForm})
#   elif request.method == 'POST':
#         adminForm = RoleForm(request.POST)
#         if adminForm.is_valid():
#             adminForm.save()
#             return HttpResponse('Korisnik je postavljen kao administrator')            
#         else:
#             return HttpResponseNotAllowed()

#autentikacija korisnika
def loginUser(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None and user.role.role == 'admin':
      login(request, user)
      return redirect('pocetna')
    elif user is not None and user.role.role == 'stud' and user.status.status == 'izvan':
      login(request, user)
      return redirect('pocetna_stud')
    elif user is not None and user.role.role == 'stud' and user.status.status == 'red':
      login(request, user)
      return redirect('pocetna_stud')
    elif user is not None and user.role.role == 'prof':
      login(request, user)
      return redirect('pocetna_prof')
    else:
      return redirect('login_user')
  else:
    return render(request, 'login.html', {})

#odjava korisnika
def logoutUser(request):
  logout(request)
  return redirect('login_user')

#pregled predmeta od strane admina
@login_required
@admin_required
def pregledPredmeta(request):
  predmeti = Predmeti.objects.all()
  paginator = Paginator(predmeti, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'pregled_predmeta.html', {'data':page_obj})

#dodavanje predmeta od strane admina
@login_required
@admin_required
def dodajPredmet(request):
  if request.method == 'GET':
    predmetForm = PredmetiForm()
    nositeljForm = NositeljForm()
    context = {'form1':predmetForm, 'form2':nositeljForm}
    return render(request, 'dodaj_predmet.html', context)
  elif request.method == 'POST':
    predmetForm = PredmetiForm(request.POST)
    nositeljForm = NositeljForm(request.POST)
    if predmetForm.is_valid():
      predmet = predmetForm.save()
      nositelj = nositeljForm.save(commit=False)
      nositelj.predmeti = predmet
      nositelj.save()
      return redirect('pregled_predmeta')
    else:
      return redirect('dodaj_predmet')

#detalji predmeta od strane admina
@login_required
@admin_required
def detaljiPredmeta(request, predmet_id):
  predmet_by_id = Predmeti.objects.get(id = predmet_id)
  nositelj = Nositelj.objects.all().filter(predmeti = predmet_id).values()[0]
  user = User.objects.all()
  return render(request, 'detalji_predmeta.html', {'data':predmet_by_id, 'data2':nositelj, 'data3':user})

#uređenje predmeta od strane admina
@login_required
@admin_required
def urediPredmet(request, predmet_id):
  predmet_by_id = Predmeti.objects.get(id = predmet_id)
  
  if request.method == 'GET':
    predmetForm = PredmetiForm(instance=predmet_by_id)
    return render(request, 'uredi_predmet.html', {'form':predmetForm})
  elif request.method == 'POST':
    predmetForm = PredmetiForm(request.POST, instance=predmet_by_id)
    if predmetForm.is_valid():
      predmetForm.save()
      return redirect('pregled_predmeta')
  else:
        return HttpResponse("Something went wrong!")

#pregled profesora od strane admina
@login_required
@admin_required
def pregledProfesora(request):
  profesori = User.objects.annotate(prof = Count('role')).filter(role__role = 'prof')
  paginator = Paginator(profesori, 4)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'pregled_profesora.html', {'data':page_obj})

#admin pocetna stranica
@login_required
@admin_required
def pocetna(request):
  return render(request, 'pocetna.html')

#dodavanje profesora od strane admina
@login_required
@admin_required
def dodajProfesora(request):
  if request.method == 'GET':
    userForm = UserForm()
    rolaForm = RoleForm()
    context = {'form1': userForm, 'form2':rolaForm}
    return render(request, 'dodaj_profesora.html', context)
  elif request.method == 'POST':
    userForm = UserForm(request.POST)
    rolaForm = RoleForm(request.POST)
    if userForm.is_valid() and rolaForm.is_valid():
      user = userForm.save()
      profile = rolaForm.save(commit=False)
      profile.user = user
      profile.save()
      return redirect('pregled_profesora')           
    else:
      return HttpResponse('<h1>Krivi unos</h1>')

#detalji profesora od strane admina
@login_required
@admin_required
def detaljiProfesor(request, profesor_id):
  user_by_id = User.objects.get(id = profesor_id)
  role_by_id = Role.objects.all().filter(user = profesor_id).values()[0]
  return render(request, 'detalji_prof.html', {'data_u':user_by_id, 'data_r':role_by_id})

#uređenje profesora od strane admina
@login_required
@admin_required
def urediProfesor(request, profesor_id):
  prof_by_id = User.objects.get(id = profesor_id)

  if request.method == 'GET':
    profForm = UserForm(instance = prof_by_id)
    context = {'form1': profForm}
    return render(request, 'uredi_prof.html', context)
  elif request.method == 'POST':
    profForm = UserForm(request.POST, instance = prof_by_id)
    if profForm.is_valid():
      profForm.save()
      return redirect('pregled_profesora')        
    else:
      profForm = UserForm(instance = prof_by_id)

#pregled studenata od strane admina
@login_required
@admin_required
def pregledStudenata(request):
  studenti = User.objects.annotate(stud = Count('role')).filter(role__role = 'stud')
  return render(request, 'pregled_studenata.html', {'data':studenti})

#redovni studenti(admin)
@login_required
@admin_required
def pregledStudenata_red(request):
  studenti = User.objects.annotate(stud = Count('role')).filter(role__role = 'stud', status__status = 'red')
  paginator = Paginator(studenti, 4)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'pregled_studenata_red.html', {'data':page_obj})

#izvanredni studenti(admin)
@login_required
@admin_required
def pregledStudenata_izvan(request):
  studenti = User.objects.annotate(stud = Count('role')).filter(role__role = 'stud', status__status = 'izvan')
  paginator = Paginator(studenti, 4)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'pregled_studenata_izvan.html', {'data':page_obj})

#dodavanje studenta od strane admina
@login_required
@admin_required
def dodajStudenta(request):
  if request.method == 'GET':
    userForm = UserForm()
    rolaForm = RoleForm()
    statusForm = StatusForm()
    context = {'form1': userForm, 'form2':rolaForm, 'form3':statusForm}
    return render(request, 'dodaj_studenta.html', context)
  elif request.method == 'POST':
    userForm = UserForm(request.POST)
    rolaForm = RoleForm(request.POST)
    statusForm = StatusForm(request.POST)
    if userForm.is_valid() and rolaForm.is_valid() and statusForm.is_valid():
      user = userForm.save()
      rola = rolaForm.save(commit=False)
      status = statusForm.save(commit=False)
      rola.user = user
      status.user = user
      rola.save()
      status.save()
      return redirect('pregled_studenata')           
    else:
      userForm = UserForm()
      rolaForm = RoleForm()
      statusForm = StatusForm()

#detalji studenta od strane admina
@login_required
@admin_required
def detaljiStudent(request, student_id):
  user_by_id = User.objects.get(id = student_id)
  role_by_id = Role.objects.all().filter(user = student_id).values()[0]
  status_by_id = Status.objects.all().filter(user = student_id).values()[0]
  return render(request, 'detalji_stud.html', {'data_u':user_by_id, 'data_r':role_by_id, 'data_s':status_by_id})

#uređenje studenta od strane admina
@login_required
@admin_required
def urediStudent(request, student_id):
  stud_by_id = User.objects.get(id = student_id)

  if request.method == 'GET':
    studForm = UserForm(instance = stud_by_id)
    context = {'form1': studForm}
    return render(request, 'uredi_stud.html', context)
  elif request.method == 'POST':
    studForm = UserForm(request.POST, instance = stud_by_id)
    if studForm.is_valid():
      studForm.save()
      return redirect('pregled_studenata')        
    else:
      studForm = UserForm(instance = stud_by_id)

#popis studenata po pojedinom predmetu od strane admina
@login_required
@admin_required
def popisStudenataPoPredmetu(request, predmet_id):
  predmet = Predmeti.objects.get(id = predmet_id)
  studenti = UpisniList.objects.all().filter(predmet = predmet_id)
  user = User.objects.all()
  context = {'predmet':predmet, 'studenti':studenti, 'user':user}
  return render(request, 'popis_studenata_po_predmetu.html', context)

#upisni list za pojedinog izvanrednog studenta 
@login_required
@student_required
def upisPredmeta_izvan(request, student_id):
  predmet_pol = Predmeti.objects.all().filter(id = 40)
  print(predmet_pol)
  predmeti = Predmeti.objects.all()
  student = User.objects.get(id = student_id)

  list_u = UpisniList.objects.all().filter(status = 'upisan', student=student.id)
  list_p = UpisniList.objects.all().filter(status = 'polozeno', student=student.id)

  lista1 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 1)
  lista2 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 2)
  lista3 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 3)
  lista4 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 4)
  lista5 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 5)
  lista6 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 6)
  lista7 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 7)
  lista8 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 8)
  context = {'predmeti':predmeti, 'list_p':list_p, 'list_u':list_u, 'lista1': lista1, 'lista2': lista2, 'lista3': lista3, 'lista4': lista4, 'lista5': lista5, 'lista6': lista6, 'lista7': lista7, 'lista8': lista8, 'student':student}

  return render(request, 'upis_predmeta_izvan.html', context)

#popis izvanrednih studenata koji su polozili i koji su upisali pojedini predmet - od strane admina
@login_required
@admin_required
def upisPredmeta_izvan_admin(request, student_id):
  predmeti = Predmeti.objects.all()
  student = User.objects.get(id = student_id)

  list_u = UpisniList.objects.all().filter(status = 'upisan', student=student.id)
  list_p = UpisniList.objects.all().filter(status = 'polozeno', student=student.id)

  lista1 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 1)
  lista2 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 2)
  lista3 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 3)
  lista4 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 4)
  lista5 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 5)
  lista6 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 6)
  lista7 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 7)
  lista8 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_izvanredni = 8)
  context = {'predmeti':predmeti, 'list_p':list_p, 'list_u':list_u, 'lista1': lista1, 'lista2': lista2, 'lista3': lista3, 'lista4': lista4, 'lista5': lista5, 'lista6': lista6, 'lista7': lista7, 'lista8': lista8, 'student':student}

  return render(request, 'upis_predmeta_izvan_admin.html', context)

#upisni list za pojedinog redovnog studenta 
@login_required
@student_required
def upisPredmeta_red(request, student_id):
  predmeti = Predmeti.objects.all()
  student = User.objects.get(id = student_id)

  list_u = UpisniList.objects.all().filter(status = 'upisan', student=student.id)
  list_p = UpisniList.objects.all().filter(status = 'polozeno', student=student.id)

  lista1 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 1)
  lista2 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 2)
  lista3 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 3)
  lista4 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 4)
  lista5 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 5)
  lista6 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 6)

  context = {'predmeti':predmeti, 'list_p':list_p, 'list_u':list_u, 'lista1': lista1, 'lista2': lista2, 'lista3': lista3, 'lista4': lista4, 'lista5': lista5, 'lista6': lista6, 'student':student}
  return render(request, 'upis_predmeta_red.html', context)

#popis redovnih studenata koji su polozili i koji su upisali pojedini predmet - od strane admina 
@login_required
@admin_required
def upisPredmeta_red_admin(request,student_id):
  predmeti = Predmeti.objects.all()
  student = User.objects.get(id = student_id)

  list_u = UpisniList.objects.all().filter(status = 'upisan', student=student.id)
  list_p = UpisniList.objects.all().filter(status = 'polozeno', student=student.id)

  lista1 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 1)
  lista2 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 2)
  lista3 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 3)
  lista4 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 4)
  lista5 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 5)
  lista6 = Predmeti.objects.exclude(upisnilist__in=UpisniList.objects.filter(student = student.id)).filter(sem_redovni = 6)

  context = {'predmeti':predmeti, 'list_p':list_p, 'list_u':list_u, 'lista1': lista1, 'lista2': lista2, 'lista3': lista3, 'lista4': lista4, 'lista5': lista5, 'lista6': lista6, 'student':student}
  return render(request, 'upis_predmeta_red_admin.html', context)

#funkcija koja studentu omogucava da se upise na pojedini predmet

@login_required
def upisi_predmet(request, predmet_id):
  user = request.user
  student_id = User.objects.get(id = user.id)
  predmet = Predmeti.objects.get(id = predmet_id)
  
  predmet_pol = Predmeti.objects.get(id = predmet_id)
  
  konacno1 = Predmeti.objects.filter(sem_redovni = 1).filter(upisnilist__status = 'polozeno').count()
  konacno2 = Predmeti.objects.filter(sem_redovni = 2).filter(upisnilist__status = 'polozeno').count()

  konacno5 = Predmeti.objects.filter(sem_izvanredni = 1).filter(upisnilist__status = 'polozeno').count()
  konacno6 = Predmeti.objects.filter(sem_izvanredni = 2).filter(upisnilist__status = 'polozeno').count()
  konacno8 = konacno5 + konacno6

  if((konacno1 + konacno2 != 8 and (predmet_pol.sem_redovni == 5 or predmet_pol.sem_redovni == 6)) or(konacno8 != 6 and(predmet_pol.sem_izvanredni == 5 or predmet_pol.sem_izvanredni == 6))):
    return HttpResponse('<h1>ne mozete upisati predmet</h1>')
  else:
    upis = UpisniList(status = 'upisan', predmet = predmet, student = student_id)
    upis.save()
    return redirect('pocetna_stud')

#funkcija koja omogucava studentu da se ispise iz pojedinog predmeta

@login_required
def ispis_iz_predmeta(request,predmet_id):
  user = request.user
  student = User.objects.get(id = user.id)
  predmet = UpisniList.objects.all().filter(predmet = predmet_id, student=student.id)
  predmet.delete()
  upit1 = UpisniList.objects.all().filter(predmet = predmet_id, student=student.id)
  return redirect('pocetna_stud')

#pregled predmeta od strane profesora
@login_required
@profesor_required
def pregledPredmetaProf(request):
  user = request.user
  profesor = User.objects.get(id = user.id)

  predmeti = Predmeti.objects.annotate(pred = Count('nositelj')).filter(nositelj__nositelj = profesor.id)
  return render(request, 'pregled_predmeta_prof.html', {'data':predmeti})

#pocetna stranica profesor
@login_required
@profesor_required
def pocetnaProfesor(request):
  return render(request, 'pocetna_prof.html')

#popis studenata koji su upisali pojedini predmet - od strane profesora
@login_required
@profesor_required
def popisStudenataPoPredmetuProf(request, predmet_id):
  predmet = Predmeti.objects.get(id = predmet_id)
  studenti = UpisniList.objects.all().filter(predmet = predmet_id)
  user = User.objects.all()
  context = {'predmet':predmet, 'studenti':studenti, 'user':user}
  return render(request, 'popis_studenata_po_predmetu_prof.html', context)

#funkcija koja omogucava promjenu statusa pregled liste studenata za koje se zeli promjenit status u polozeno
@login_required
@profesor_required
def promjenaStatusa(request, predmet_id):
  predmet = Predmeti.objects.get(id = predmet_id)
  studenti = UpisniList.objects.all().filter(predmet = predmet_id)
  user = User.objects.all()
  context = {'predmet':predmet, 'studenti':studenti, 'user':user}
  return render(request, 'promjena_statusa.html', context)

#funkcija koja omogucava promjenu statusa predmeta za studenta u polozeno - od strane profesora
@login_required
def statusPolozi(request, predmet_id, student_id):
  status = 'polozeno'
  UpisniList.objects.filter(predmet = predmet_id, student = student_id).update(status = status)
  return redirect('pregled_predmeta_prof')

#funkcija koja omogucava pregled studenata koji su polozili predmet - od strane profesora
@login_required
@profesor_required
def popisPolozenih(request, predmet_id):
  predmet = Predmeti.objects.get(id = predmet_id)
  studenti = UpisniList.objects.all().filter(predmet = predmet_id)
  user = User.objects.all()
  context = {'predmet':predmet, 'studenti':studenti, 'user':user}
  return render(request, 'popis_polozenih.html', context)

#funkcija koja omogucava adminu da promjeni status iz polozeno u upisano
@login_required
def statusUpisan(request, predmet_id, student_id):
  status = 'upisan'
  UpisniList.objects.filter(predmet = predmet_id, student = student_id).update(status = status)
  return redirect('pregled_studenata')

#pocetna stranica za studenta
@login_required
@student_required
def pocetna_student(request):
  return render(request, 'pocetna_stud.html')

def popis_trece(request):
  redovni = User.objects.filter(status__status = 'red')
  izvanredni = User.objects.filter(status__status = 'izvan').annotate(count = Count('upisnilist')).filter(upisnilist__status = 'upisan')
  predmet = Predmeti.objects.filter(sem_redovni = 5).annotate(count = Count('upisnilist')).filter(upisnilist__status = 'upisan')
  upis = UpisniList.objects.all()

  return render(request, 'popis_trece.html', {'redovni':redovni, 'izvanredni': izvanredni, 'predmet':predmet, 'upis':upis})

























































# def upisPredmeta_red(request, student_id):
#   predmeti = Predmeti.objects.all()
#   student = User.objects.get(id = student_id)

#   list_u = UpisniList.objects.all().filter(status = 'upisan', student=student.id)
#   list_p = UpisniList.objects.all().filter(status = 'polozeno', student=student.id)

#   lista1 = Predmeti.objects.filter(sem_redovni = 1).exclude(upisnilist__student_id__in=[student.id])
#   lista2 = Predmeti.objects.exclude(upisnilist__student_id__in=[student.id]).filter(sem_redovni = 2)
#   lista3 = Predmeti.objects.exclude(upisnilist__student_id__in=[student.id]).filter(sem_redovni = 3)
#   lista4 = Predmeti.objects.exclude(upisnilist__student_id__in=[student.id]).filter(sem_redovni = 4)
#   lista5 = Predmeti.objects.exclude(upisnilist__student_id__in=[student.id]).filter(sem_redovni = 5)
#   lista6 = Predmeti.objects.exclude(upisnilist__student_id__in=[student.id]).filter(sem_redovni = 6)

