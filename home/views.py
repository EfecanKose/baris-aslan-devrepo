from bootstrap_modal_forms.generic import BSModalFormView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from post.forms import PostForm, Form2
from post.models import Post, Notification, Yayinevi
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic import View
import io
import xlsxwriter
from django.urls import reverse_lazy



def home_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'home.html', context)


def data_table(request):
    notifications = request.user.notification_set.all()
    notifications_unread = Notification.objects.filter(read=False).count()
    for notification in notifications:
        notification.read = True
        notification.save()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Post modelindeki kullanıcıyı ayarlar
            post.save()  # Verileri kaydet.
            return redirect('data_table')  # Yönlendirme yaparak formu kaydettiğiniz sayfaya git
    else:
        form = PostForm()
    posts = Post.objects.all()
    context = {'form': form, 'posts': posts, 'notifications': notifications,
               'unread': notifications_unread}  # Form ve tüm Post örneklerini gönder

    return render(request, 'datatables.html', context)


def ItemListView(request):
    # DataTables parametrelerini ayıklama
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    search_value = request.GET.get('search[value]', '')

    # Post nesnelerini DataTables parametrelerine göre sorgula
    posts = Post.objects.all()

    if search_value:
        posts = posts.filter(Q(title__icontains=search_value) | Q(id__icontains=search_value))

    if order_dir == 'asc':
        order_column = Post._meta.fields[order_column].name
    else:
        order_column = '-' + Post._meta.fields[order_column].name
    posts = posts.order_by(order_column)

    # Pagination
    paginator = Paginator(posts, length)
    page = (start // length) + 1
    posts = paginator.get_page(page)

    # JSON formatındaki sorgu sonuçlarını dönüştürme
    data = []
    for post in posts:
        data.append({
            'username': post.user.username,
            'title': post.title,
            'content': post.content,
            'publishing_date': post.publishing_date,
            'yayin': post.yayin.ad,
            'onay': post.onay,
        })

    response = {
        'draw': int(request.GET.get('draw', 1)),
        'recordsTotal': Post.objects.count(),
        'recordsFiltered': posts.paginator.count,
        'data': data,
    }

    return JsonResponse(response)


class ExportExcelView(View):
    def get(self, request, *args, **kwargs):
        data = Post.objects.all()

        # Verileri Excel'e aktar
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Tablo başlıkları
        columns = ['username', 'title', 'content', 'publishing_date']
        row_num = 0
        for col_num, column_title in enumerate(columns):
            worksheet.write(row_num, col_num, column_title)

        # Verileri tabloya yaz
        for row in data:
            row_num += 1
            row = [row.user.username, row.title, row.content, row.publishing_date]
            for col_num, cell_value in enumerate(row):
                worksheet.write(row_num, col_num, cell_value)

        workbook.close()
        output.seek(0)

        # Response ayarları
        response = HttpResponse(output.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=export.xlsx'
        return response











