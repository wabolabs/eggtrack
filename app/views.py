from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Q, Count
from django.contrib.auth.decorators import login_required
from .models import Hen, EggLog, Breed, Color
from django import forms


class EggLogForm(forms.Form):
    def __init__(self, *args, **kwargs):
        hens = kwargs.pop('hens', [])
        today_logs = kwargs.pop('today_logs', {})
        super().__init__(*args, **kwargs)
        for hen in hens:
            self.fields[f'hen_{hen.id}'] = forms.IntegerField(
                label=hen.name,
                initial=today_logs.get(hen.id, 0),
                min_value=0,
                max_value=100
            )


@login_required
def daily_log(request):
    today = timezone.localdate()
    hen_list = Hen.objects.filter(is_active=True).order_by('name')
    
    if request.method == 'POST':
        form = EggLogForm(request.POST, hens=hen_list, today_logs={})
        if form.is_valid():
            for hen in hen_list:
                quantity = form.cleaned_data.get(f'hen_{hen.id}', 0)
                if quantity > 0:
                    EggLog.objects.update_or_create(
                        hen=hen,
                        date=today,
                        defaults={'quantity': quantity}
                    )
            return redirect('daily_log')
    
    today_logs = EggLog.objects.filter(date=today).values_list('hen_id', 'quantity')
    today_logs_dict = {item[0]: item[1] for item in today_logs}
    
    form = EggLogForm(hens=hen_list, today_logs=today_logs_dict)
    
    return render(request, 'app/daily_log.html', {
        'title': 'Daily Log',
        'hens': hen_list,
        'today': today,
        'form': form,
    })


@login_required
def hen_list(request):
    hens = Hen.objects.all().order_by('name')
    return render(request, 'app/hen_list.html', {'title': 'Hens', 'hens': hens})


@login_required
def hen_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        breed_id = request.POST.get('breed')
        color_id = request.POST.get('color')
        photo = request.FILES.get('photo')
        
        breed = Breed.objects.get(id=breed_id) if breed_id else None
        color = Color.objects.get(id=color_id) if color_id else None
        
        Hen.objects.create(name=name, breed=breed, color=color, photo=photo)
        return redirect('hen_list')
    
    breeds = Breed.objects.all()
    colors = Color.objects.all()
    return render(request, 'app/hen_add.html', {'title': 'Add Hen', 'breeds': breeds, 'colors': colors})


@login_required
def hen_update_photo(request, hen_id):
    hen = get_object_or_404(Hen, id=hen_id)
    
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        if photo:
            hen.photo = photo
            hen.save()
        return redirect('hen_list')
    
    return render(request, 'app/hen_update_photo.html', {'title': f'Update Photo — {hen.name}', 'hen': hen})


@login_required
def stats(request):
    hens = Hen.objects.filter(is_active=True)
    breeds = Breed.objects.all()
    colors = Color.objects.all()
    
    # Default: last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    selected_hens = request.GET.getlist('hen')
    selected_breeds = request.GET.getlist('breed')
    selected_colors = request.GET.getlist('color')
    date_range = request.GET.get('date_range', '30')
    
    if date_range == '7':
        start_date = end_date - timedelta(days=7)
    elif date_range == '90':
        start_date = end_date - timedelta(days=90)
    elif date_range == '365':
        start_date = end_date - timedelta(days=365)
    
    queryset = EggLog.objects.filter(date__range=[start_date, end_date])
    
    if selected_hens:
        queryset = queryset.filter(hen_id__in=selected_hens)
    if selected_breeds:
        queryset = queryset.filter(hen__breed_id__in=selected_breeds)
    if selected_colors:
        queryset = queryset.filter(hen__color_id__in=selected_colors)
    
    stats_data = []
    
    for hen in hens:
        if selected_hens and hen.id not in [int(h) for h in selected_hens]:
            continue
            
        hen_queryset = queryset.filter(hen=hen)
        total_eggs = hen_queryset.aggregate(total=Sum('quantity'))['total'] or 0
        days_in_range = (end_date - start_date).days + 1
        daily_avg = total_eggs / days_in_range if days_in_range else 0
        
        stats_data.append({
            'hen': hen,
            'total_eggs': total_eggs,
            'daily_avg': round(daily_avg, 2),
            'days_laid': hen_queryset.values('date').distinct().count(),
        })
    
    # Summary stats
    total_eggs_all = queryset.aggregate(total=Sum('quantity'))['total'] or 0
    
    return render(request, 'app/stats.html', {
        'title': 'Statistics',
        'stats_data': stats_data,
        'hens': hens,
        'breeds': breeds,
        'colors': colors,
        'selected_hens': selected_hens,
        'selected_breeds': selected_breeds,
        'selected_colors': selected_colors,
        'date_range': date_range,
        'total_eggs_all': total_eggs_all,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
def edit_history(request):
    selected_hen = request.GET.get('hen')
    selected_breed = request.GET.get('breed')
    selected_color = request.GET.get('color')
    search_date = request.GET.get('date')
    
    if search_date:
        try:
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
        except ValueError:
            search_date = None
    
    queryset = EggLog.objects.select_related('hen').all()
    
    if selected_hen:
        queryset = queryset.filter(hen_id=selected_hen)
    if selected_breed:
        queryset = queryset.filter(hen__breed_id=selected_breed)
    if selected_color:
        queryset = queryset.filter(hen__color_id=selected_color)
    if search_date:
        queryset = queryset.filter(date=search_date)
    
    queryset = queryset.order_by('-date', 'hen__name')
    
    hens = Hen.objects.filter(is_active=True)
    breeds = Breed.objects.all()
    colors = Color.objects.all()
    
    if request.method == 'POST':
        log_id = request.POST.get('log_id')
        action = request.POST.get('action')
        
        if log_id and action:
            log = get_object_or_404(EggLog, id=log_id)
            
            if action == 'update':
                quantity = request.POST.get('quantity', 1)
                try:
                    log.quantity = int(quantity)
                    log.save()
                except (ValueError, TypeError):
                    pass
            elif action == 'delete':
                log.delete()
        
        return redirect('edit_history')
    
    return render(request, 'app/edit_history.html', {
        'title': 'Edit History',
        'logs': queryset,
        'hens': hens,
        'breeds': breeds,
        'colors': colors,
        'selected_hen': selected_hen,
        'selected_breed': selected_breed,
        'selected_color': selected_color,
        'search_date': search_date,
    })


@login_required
def breed_list(request):
    breeds = Breed.objects.all()
    return render(request, 'app/breed_list.html', {'title': 'Breeds', 'breeds': breeds})


@login_required
def breed_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        Breed.objects.create(name=name, description=description)
        return redirect('breed_list')
    
    return render(request, 'app/breed_add.html', {'title': 'Add Breed'})


@login_required
def color_list(request):
    colors = Color.objects.all()
    return render(request, 'app/color_list.html', {'title': 'Colors', 'colors': colors})


@login_required
def color_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        Color.objects.create(name=name, description=description)
        return redirect('color_list')
    
    return render(request, 'app/color_add.html', {'title': 'Add Color'})
