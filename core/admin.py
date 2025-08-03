from django.contrib import admin
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import (
    Measure, FiscalQuarter, Period, FiscalYear, FiscalYearPeriod,
    PeriodMonth, AccountType, Organisation, Account,
    Project,
    FinancialData,
)


class LevelAndParentFilter(admin.SimpleListFilter):
    title = _('Depth')
    parameter_name = 'depth'

    def lookups(self, request, model_admin):
        depths = model_admin.model.objects.values_list('depth', flat=True).distinct().order_by('depth')
        return [(depth, f'Depth {depth}') for depth in depths]

    def queryset(self, request, queryset):
        if self.value():
            parents = queryset.filter(depth=self.value())
            descendants = queryset.none()

            # Check if we are showing all descendants or just children
            show_descendants = request.GET.get('descendants', 'children') == 'descendants'

            for parent in parents:
                if show_descendants:
                    descendants |= parent.get_descendants()
                else:
                    descendants |= parent.get_children()  # Direct children only

            return parents | descendants
        return queryset


class DepthFilter(admin.SimpleListFilter):
    title = _('Depth Limit')
    parameter_name = 'depth_limit'

    def lookups(self, request, model_admin):
        # Get the current depth selected
        current_depth = request.GET.get('depth')
        if current_depth:
            # Provide lookups from current_depth +1 to max depth
            max_depth = model_admin.model.objects.aggregate(max_depth=Max('depth'))['max_depth']
            return [(str(depth), f'Depth {depth}') for depth in range(int(current_depth) + 1, max_depth + 1)]
        return []

    def queryset(self, request, queryset):
        # If a depth limit is selected, filter accordingly
        depth_limit = self.value()
        if depth_limit:
            return queryset.filter(depth__lte=depth_limit)
        return queryset


class ChildrenOrDescendantsFilter(admin.SimpleListFilter):
    title = _('Show Descendants')
    parameter_name = 'descendants'

    def lookups(self, request, model_admin):
        return [
            ('children', 'Children Only'),
            ('descendants', 'All Descendants')
        ]

    def queryset(self, request, queryset):
        return queryset  # This will be used later in combination with LevelAndParentFilter

# Admin for Treebeard Models
class AccountTypeAdmin(TreeAdmin):
    form = movenodeform_factory(AccountType)
    ordering = ['path']


admin.site.register(AccountType, AccountTypeAdmin)


class AccountAdmin(TreeAdmin):
    form = movenodeform_factory(Account)
    list_filter = (LevelAndParentFilter, ChildrenOrDescendantsFilter, DepthFilter)

    ordering = ['path']

    def get_parent_from_path(self, instance):
        # Derive parent path by removing the last `steplen` characters from `path`
        if len(instance.path) > instance.steplen:
            parent_path = instance.path[:-instance.steplen]
            return self.model.objects.filter(path=parent_path).first()
        return None


admin.site.register(Account, AccountAdmin)


class FiscalYearPeriodAdmin(admin.ModelAdmin):
    # Specify the fields to display in the form
    fields = ['fiscal_year', 'period', 'open', 'default_budget']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # If a FiscalYearPeriod object exists (in case of editing), set its fiscal_year
        if obj:
            fiscal_year = obj.fiscal_year
        else:
            fiscal_year = None

        # Dynamically modify the queryset for 'period' field based on the selected fiscal year
        if fiscal_year:
            # Filter out periods that have already been used for the selected fiscal year
            used_periods = FiscalYearPeriod.objects.filter(fiscal_year=fiscal_year).values_list('period', flat=True)
            form.base_fields['period'].queryset = Period.objects.exclude(id__in=used_periods)
        else:
            # If no fiscal year is selected yet, show all periods
            form.base_fields['period'].queryset = Period.objects.all()

        return form


admin.site.register(FiscalYearPeriod, FiscalYearPeriodAdmin)


class OrganisationAdmin(TreeAdmin):
    form = movenodeform_factory(Organisation)
    list_filter = (LevelAndParentFilter, ChildrenOrDescendantsFilter, DepthFilter)

    ordering = ['path']

    def get_parent_from_path(self, instance):
        # Derive parent path by removing the last `steplen` characters from `path`
        if len(instance.path) > instance.steplen:
            parent_path = instance.path[:-instance.steplen]
            return self.model.objects.filter(path=parent_path).first()
        return None


admin.site.register(Organisation, OrganisationAdmin)


class ProjectAdmin(TreeAdmin):
    form = movenodeform_factory(Organisation)
    list_filter = (LevelAndParentFilter, ChildrenOrDescendantsFilter, DepthFilter)

    ordering = ['path']

    def get_parent_from_path(self, instance):
        # Derive parent path by removing the last `steplen` characters from `path`
        if len(instance.path) > instance.steplen:
            parent_path = instance.path[:-instance.steplen]
            return self.model.objects.filter(path=parent_path).first()
        return None


admin.site.register(Project, ProjectAdmin)
admin.site.register(Measure)
admin.site.register(FiscalQuarter)
admin.site.register(Period)
admin.site.register(FiscalYear)
admin.site.register(PeriodMonth)
admin.site.register(FinancialData)
