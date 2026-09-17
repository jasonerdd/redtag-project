from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from openpyxl import Workbook

from .models import RedTag, Station, IssueType, Employee
from .forms import RedTagForm, RedTagFilterForm


class RedTagListView(LoginRequiredMixin, ListView):
    model = RedTag
    template_name = 'tags/redtag_list.html'
    context_object_name = 'redtags'
    paginate_by = 25

    def get_queryset(self):
        qs = RedTag.objects.select_related(
            'vehicle', 'vehicle__model', 'vehicle__dealer', 'section', 'station',
            'category', 'issue_type', 'raised_by', 'verified_by'
        ).all()

        status = self.request.GET.get('status')
        section = self.request.GET.get('section')
        model = self.request.GET.get('model')
        chassis = self.request.GET.get('chassis')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        q = self.request.GET.get('q')

        if status:
            qs = qs.filter(status=status)
        if section:
            qs = qs.filter(section_id=section)
        if model:
            qs = qs.filter(vehicle__model_id=model)
        if chassis:
            qs = qs.filter(vehicle__chassis_no__icontains=chassis)
        if date_from:
            qs = qs.filter(date_raised__gte=date_from)
        if date_to:
            qs = qs.filter(date_raised__lte=date_to)
        if q:
            qs = qs.filter(
                Q(issue_description__icontains=q)
                | Q(part_number__icontains=q)
                | Q(part_name__icontains=q)
                | Q(vehicle__chassis_no__icontains=q)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = RedTagFilterForm(self.request.GET or None)
        context['query'] = self.request.GET.get('q', '')
        return context


class RedTagDetailView(LoginRequiredMixin, DetailView):
    model = RedTag
    template_name = 'tags/redtag_detail.html'
    context_object_name = 'redtag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.filter(active=True)
        return context


class RedTagCreateView(LoginRequiredMixin, CreateView):
    model = RedTag
    form_class = RedTagForm
    template_name = 'tags/redtag_form.html'
    success_url = reverse_lazy('redtag-create')

    def get_initial(self):
        initial = super().get_initial()
        initial.setdefault('date_raised', timezone.localdate())
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Red tag saved. You can enter another one below.')
        return super().form_valid(form)


class RedTagUpdateView(LoginRequiredMixin, UpdateView):
    model = RedTag
    form_class = RedTagForm
    template_name = 'tags/redtag_form.html'
    success_url = reverse_lazy('redtag-list')

    def form_valid(self, form):
        messages.success(self.request, 'Red tag updated successfully.')
        return super().form_valid(form)


@login_required
def close_redtag(request, pk):
    redtag = get_object_or_404(RedTag, pk=pk)
    if request.method == 'POST':
        verified_by_id = request.POST.get('verified_by')
        if not verified_by_id:
            messages.error(request, 'Select who verified/cleared this tag.')
            return redirect('redtag-detail', pk=pk)

        redtag.status = RedTag.STATUS_CLOSED
        redtag.closing_date = timezone.localdate()
        redtag.verified_by_id = verified_by_id
        remarks = request.POST.get('remarks', '').strip()
        if remarks:
            redtag.remarks = remarks
        redtag.save()
        messages.success(request, f'Red tag #{redtag.pk} closed.')
    return redirect('redtag-detail', pk=pk)


@login_required
def export_redtags(request):
    qs = RedTag.objects.select_related(
        'vehicle', 'vehicle__model', 'vehicle__dealer', 'section', 'station',
        'category', 'issue_type', 'raised_by', 'verified_by'
    ).all()

    status = request.GET.get('status')
    section = request.GET.get('section')
    model = request.GET.get('model')
    chassis = request.GET.get('chassis')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if status:
        qs = qs.filter(status=status)
    if section:
        qs = qs.filter(section_id=section)
    if model:
        qs = qs.filter(vehicle__model_id=model)
    if chassis:
        qs = qs.filter(vehicle__chassis_no__icontains=chassis)
    if date_from:
        qs = qs.filter(date_raised__gte=date_from)
    if date_to:
        qs = qs.filter(date_raised__lte=date_to)

    wb = Workbook()
    ws = wb.active
    ws.title = 'Red Tag'
    headers = [
        'Date', 'Section', 'Dealer', 'Model', 'Lot', 'Chassis no.',
        'Part Number', 'Part Name', 'Qnty', 'Issue Description',
        'Category', 'Issue Type', 'Reason Code', 'Raised By', 'Station',
        'Action', 'Status', 'Closing Date', 'Cleared / Verified By',
        'Remarks', 'Location', 'VIN Size',
    ]
    ws.append(headers)

    for tag in qs.iterator(chunk_size=2000):
        ws.append([
            tag.date_raised,
            tag.section.code if tag.section_id else '',
            tag.vehicle.dealer.name if tag.vehicle.dealer_id else '',
            tag.vehicle.model.name if tag.vehicle.model_id else '',
            tag.vehicle.lot,
            tag.vehicle.chassis_no,
            tag.part_number,
            tag.part_name,
            tag.quantity,
            tag.issue_description,
            tag.category.name if tag.category_id else '',
            tag.issue_type.name if tag.issue_type_id else '',
            tag.reason_code,
            tag.raised_by.employee_no if tag.raised_by_id else '',
            tag.station.name if tag.station_id else '',
            tag.action_taken,
            tag.status,
            tag.closing_date,
            tag.verified_by.employee_no if tag.verified_by_id else '',
            tag.remarks,
            tag.location,
            tag.vehicle.vi_size,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="red_tag_export.xlsx"'
    wb.save(response)
    return response


def load_stations(request):
    section_id = request.GET.get('section_id')
    stations = Station.objects.filter(
        section_id=section_id, show_in_form=True
    ).order_by('name')
    data = [{'id': s.id, 'name': s.name} for s in stations]
    return JsonResponse(data, safe=False)


def load_issue_types(request):
    category_id = request.GET.get('category_id')
    issue_types = IssueType.objects.filter(category_id=category_id).order_by('name')
    data = [{'id': i.id, 'name': i.name} for i in issue_types]
    return JsonResponse(data, safe=False)
