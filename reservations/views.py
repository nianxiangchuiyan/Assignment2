from datetime import datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localtime, make_aware
from django.views import View

from .forms import CustomUserCreationForm
from .models import Room, Reservation


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user = form.save()
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)  # profile
                return redirect('home')  # redirect to home
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # or redirect to home


class ProfileDetail(View):
    template_name = 'profile_detail.html'

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user).order_by('start_time')

        # 生成标准时间段列表
        time_list = []
        now = timezone.localtime()
        today = timezone.localdate()

        start = make_aware(datetime.combine(today, time(8, 0)))
        for i in range(21):  # 20个半小时格子+18:00
            slot_time = start + timedelta(minutes=i * 30)
            if today == now.date() and slot_time <= now - timedelta(minutes=30):
                continue  # 如果是今天且已经过去，就跳过
            time_list.append(slot_time.strftime("%H:%M"))
        return render(request, self.template_name, {
            'reservations': reservations,
            'time_options': time_list,
            'time_options_end': time_list[1:],
            'time_options_start': time_list[:-1], }
                      )

    def post(self, request):
        action = request.POST.get('action')
        res_id = request.POST.get('reservation_id')

        if action and res_id:
            reservation = get_object_or_404(Reservation, id=res_id, user=request.user)

            if action == 'cancel':
                reservation.delete()
                messages.success(request, "Reservation cancelled successfully!")
            elif action == 'edit':
                new_start = request.POST.get('start_time')
                new_end = request.POST.get('end_time')

                try:
                    new_start_dt = datetime.combine(reservation.start_time.date(),
                                                    datetime.strptime(new_start, "%H:%M").time())
                    new_end_dt = datetime.combine(reservation.start_time.date(),
                                                  datetime.strptime(new_end, "%H:%M").time())

                    new_start_dt = timezone.make_aware(new_start_dt)
                    new_end_dt = timezone.make_aware(new_end_dt)

                    # 检查冲突
                    conflict = Reservation.objects.filter(
                        room=reservation.room,
                        start_time__lt=new_end_dt,
                        end_time__gt=new_start_dt
                    ).exclude(id=reservation.id).exists()

                    if conflict:
                        messages.error(request, "The selected time conflicts with another reservation.")
                    else:
                        reservation.start_time = new_start_dt
                        reservation.end_time = new_end_dt
                        reservation.save()
                        messages.success(request, "Reservation updated successfully!")

                except ValueError:
                    messages.error(request, "Invalid time format.")

        return redirect('profile_detail')


@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


@login_required
def make_reservation(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    today = timezone.localdate()

    # 获取今天已有预约时间段
    reservations = Reservation.objects.filter(room=room, start_time__date=today)
    booked_slots = set()

    for res in reservations:

        start_local = localtime(res.start_time)
        end_local = localtime(res.end_time)

        start_idx = (start_local.hour - 8) * 2 + (0 if start_local.minute < 30 else 1)
        end_idx = (end_local.hour - 8) * 2 + (0 if end_local.minute < 30 else 1)

        for i in range(start_idx, end_idx):
            booked_slots.add(i)

    # 构建 slots 数据：供模板渲染时间格子
    slots = []
    current = time(8, 0)
    for i in range(20):
        label = current.strftime("%H:%M")
        status = "booked" if i in booked_slots else "available"
        slots.append({"time": label, "status": status})
        # 加 30 分钟
        dt = datetime.combine(today, current) + timedelta(minutes=30)
        current = dt.time()

    # POST 请求：处理预约
    if request.method == "POST":
        start_str = request.POST.get("start_time")  # 格式如 "13:00"
        end_str = request.POST.get("end_time")  # 格式如 "13:30"
        if start_str and end_str:
            try:
                start_dt = datetime.combine(today, datetime.strptime(start_str, "%H:%M").time())
                end_dt = datetime.combine(today, datetime.strptime(end_str, "%H:%M").time())

                conflict = Reservation.objects.filter(
                    room=room,
                    start_time__lt=end_dt,
                    end_time__gt=start_dt
                ).exists()

                if conflict:
                    messages.error(request, "This time range is already booked. Please try another one.")
                else:

                    Reservation.objects.create(
                        user=request.user,
                        room=room,
                        start_time=start_dt,
                        end_time=end_dt
                    )
                    messages.success(request, "Reservation confirmed!")
                    return redirect('make_reservation', room_id=room.id)
            except ValueError:
                messages.error(request, "Invalid time format.")

    return render(request, "make_reservation.html", {
        "room": room,
        "slots": slots,
        "today": today
    })


@login_required()
def room_schedule(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    today = timezone.localdate()  # today's date in current timezone
    # Get all reservations for this room today
    reservations = Reservation.objects.filter(room=room, start_time__date=today)
    # Determine which half-hour slots (indices 0-19) are booked
    booked_slots = set()
    for res in reservations:
        # Compute slot indices for reservation's time range
        start_idx = (res.start_time.hour - 8) * 2 + (0 if res.start_time.minute < 30 else 1)
        end_idx = (res.end_time.hour - 8) * 2 + (0 if res.end_time.minute < 30 else 1)
        # Mark all slots from start_idx up to (end_idx - 1) as booked
        for idx in range(start_idx, end_idx):
            booked_slots.add(idx)
    # Build list of slots with time labels and status
    slots = []
    current_time = time(8, 0)  # start at 08:00
    for i in range(20):
        slot_label = current_time.strftime("%H:%M")
        status = "booked" if i in booked_slots else "available"
        slots.append({"time": slot_label, "status": status})
        # increment time by 30 minutes
        hour, minute = current_time.hour, current_time.minute
        minute += 30
        if minute == 60:
            hour += 1
            minute = 0
        current_time = time(hour, minute)
    # Handle form submission (if user submitted a new booking)
    if request.method == "POST":
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")

        # Convert these strings to datetime objects (on today's date) and save new Reservation
        # (Omitted: validation to ensure no conflict and creating the reservation)
        # ...
    # Render template with slots and room inforeturn redirect('make_reservation', room_id=room.id)
    return render(request, "room_schedule.html", {"room": room, "slots": slots})


@login_required
def all_rooms_view(request):
    date_str = request.GET.get("date")
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    rooms = Room.objects.all()
    all_data = []

    now = timezone.localtime().replace(tzinfo=None)

    for room in rooms:
        reservations = Reservation.objects.filter(room=room, start_time__date=selected_date)
        booked = set()
        for res in reservations:
            start_local = localtime(res.start_time)
            end_local = localtime(res.end_time)

            start_idx = (start_local.hour - 8) * 2 + (0 if start_local.minute < 30 else 1)
            end_idx = (end_local.hour - 8) * 2 + (0 if end_local.minute < 30 else 1)

            for i in range(start_idx, end_idx):
                booked.add(i)

        slots = []
        current = datetime.combine(selected_date, time(8, 0))
        for i in range(20):
            label = current.time().strftime("%H:%M")
            status = "booked" if i in booked else "available"

            if selected_date == timezone.localdate() and (current + timedelta(minutes=30)) <= now:
                status = "past"

            slots.append({"time": label, "status": status})
            current += timedelta(minutes=30)

        all_data.append({"room": room, "slots": slots})

    slots_header = []
    start_time = datetime.strptime("08:00", "%H:%M")
    for i in range(20):
        slots_header.append((start_time + timedelta(minutes=i * 30)).strftime("%H:%M"))

    if request.method == "POST":
        room_id = request.POST.get("room_id")
        start_str = request.POST.get("start_time")
        end_str = request.POST.get("end_time")
        date_str = request.POST.get("current_date")

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            if selected_date != timezone.localdate():
                selected_date = selected_date
        if room_id and start_str and end_str:
            room = get_object_or_404(Room, pk=room_id)
            try:
                start_naive = datetime.combine(selected_date, datetime.strptime(start_str, "%H:%M").time())
                end_naive = datetime.combine(selected_date, datetime.strptime(end_str, "%H:%M").time())

                # timezone aware
                start_dt = timezone.make_aware(start_naive)
                end_dt = timezone.make_aware(end_naive)

                conflict = Reservation.objects.filter(
                    room=room,
                    start_time__lt=end_dt,
                    end_time__gt=start_dt
                ).exists()

                if not conflict:
                    Reservation.objects.create(
                        user=request.user,
                        room=room,
                        start_time=start_dt,
                        end_time=end_dt
                    )
                    messages.success(request, f"Reservation successful!")
                    return redirect(f"{reverse('all_rooms')}?date={selected_date}")
                else:
                    messages.error(request, "Time slot already booked.")
            except Exception as e:
                print(e)
                messages.error(request, "Invalid time input.")

    return render(request, "all_rooms.html", {
        "all_data": all_data,
        "slots_header": slots_header,
        "selected_date": selected_date,
        "prev_date": selected_date - timedelta(days=1),
        "next_date": selected_date + timedelta(days=1),
        "today": timezone.localdate(),
    })

