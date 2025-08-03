from django.db import models
from treebeard.mp_tree import MP_Node


class MeasureManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Measure(models.Model):
    name = models.CharField(max_length=186, db_index=True, unique=True)

    objects = MeasureManager()
    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name


class FiscalQuarterManager(models.Manager):
    def get_by_natural_key(self, quarter):
        return self.get(quarter=quarter)


class FiscalQuarter(models.Model):

    class FiscalQuarterChoices(models.IntegerChoices):
        Q1 = 1, 'Q1'
        Q2 = 2, 'Q2'
        Q3 = 3, 'Q3'
        Q4 = 4, 'Q4'
        SP = 5, 'Special Periods'

    quarter = models.IntegerField(
        choices=FiscalQuarterChoices,
        default=FiscalQuarterChoices.Q1,
        db_index=True,
        unique=True,
    )

    objects = FiscalQuarterManager()

    def natural_key(self):
        return (self.quarter,)

    def __str__(self):
        return self.get_quarter_display()


class PeriodManager(models.Manager):
    def get_by_natural_key(self, period):
        return self.get(period=period)


class Period(models.Model):

    class PeriodChoices(models.IntegerChoices):
        P01 = 1, 'Period 01'
        P02 = 2, 'Period 02'
        P03 = 3, 'Period 03'
        P04 = 4, 'Period 04'
        P05 = 5, 'Period 05'
        P06 = 6, 'Period 06'
        P07 = 7, 'Period 07'
        P08 = 8, 'Period 08'
        P09 = 9, 'Period 09'
        P10 = 10, 'Period 10'
        P11 = 11, 'Period 11'
        P12 = 12, 'Period 12'
        P13 = 13, 'Period 13'
        P14 = 14, 'Period 14'
        P15 = 15, 'Period 15'
        P16 = 16, 'Period 16'

    period = models.IntegerField(choices=PeriodChoices.choices, db_index=True, unique=True)
    quarter = models.ForeignKey(FiscalQuarter, db_index=True, on_delete=models.PROTECT)

    objects = PeriodManager()

    def natural_key(self):
        return (self.period,)

    def __str__(self):
        return self.get_period_display()


class FiscalYearManager(models.Manager):
    def get_by_natural_key(self, start_date):
        return self.get(start_date=start_date)


class FiscalYear(models.Model):
    start_date = models.DateField(db_index=True, unique=True)
    end_date = models.DateField()

    @property
    def fiscal_year(self):
        # If the year runs from January 1 to December 31, return the end year
        if self.start_date.month == 1 and self.end_date.month == 12:
            return format(self.end_date, 'Y')
        # Otherwise, return a range from the start year to the end year
        return f"{format(self.start_date, '%Y')}-{format(self.end_date, '%y')}"

    objects = FiscalYearManager()

    def natural_key(self):
        return (self.start_date,)

    def __str__(self):
        return self.fiscal_year


class FiscalYearPeriodManager(models.Manager):
    def get_by_natural_key(self, fiscal_year, period):
        return self.get(fiscal_year=fiscal_year, period=period)


class FiscalYearPeriod(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.PROTECT)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    open = models.BooleanField(default=False) # Open for posting
    default_budget = models.ForeignKey(Measure, on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'code__in': [3, 4]})

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'fiscal_year',
                    'period'
                ], name='unique_fiscal_year_period'
            )
        ]

    objects = FiscalYearPeriodManager()

    def natural_key(self):
        return (self.fiscal_year, self.period)

    def __str__(self):
        return f"{self.fiscal_year} - {self.period}. Open: {self.open}"


class PeriodMonthManager(models.Manager):
    def get_by_natural_key(self, period):
        return self.get(period=period)


class PeriodMonth(models.Model):
    class MonthChoices(models.IntegerChoices):
        JAN = 1, 'January'
        FEB = 2, 'February'
        MAR = 3, 'March'
        APR = 4, 'April'
        MAY = 5, 'May'
        JUN = 6, 'June'
        JUL = 7, 'July'
        AUG = 8, 'August'
        SEP = 9, 'September'
        OCT = 10, 'October'
        NOV = 11, 'November'
        DEC = 12, 'December'

    period = models.OneToOneField(Period, on_delete=models.PROTECT, db_index=True)
    month = models.IntegerField(choices=MonthChoices.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['period', 'month'],
                name='unique_period_month'
            )
        ]

    objects = PeriodMonthManager()

    def natural_key(self):
        return (self.period,)

    def __str__(self):
        return f"{self.period}|{self.get_short_month}"

    @property
    def get_long_month(self):
        return self.get_month_display()

    @property
    def get_short_month(self):
        month_short_map = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        return month_short_map.get(self.month, 'Unknown')


class AccountTypeManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class AccountType(MP_Node):
    class OperatorChoices(models.IntegerChoices):
        DEBIT = 1, 'DR'
        CREDIT = -1, 'CR'

    code = models.PositiveSmallIntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=20, unique=True)
    operator = models.SmallIntegerField(choices=OperatorChoices)
    node_order_by = ['code']

    objects = AccountTypeManager()

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return f"{self.code}|{self.name}"


class OrganisationManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Organisation(MP_Node):
    code = models.CharField(max_length=7, db_index=True, unique=True)
    name = models.CharField(max_length=80, unique=True)
    # level = models.PositiveIntegerField(db_index=True, default=0)
    active_from = models.ForeignKey(FiscalYearPeriod, on_delete=models.PROTECT, related_name='organisation_active_from')
    active_to = models.ForeignKey(FiscalYearPeriod, on_delete=models.PROTECT, related_name='organisation_active_to', null=True, blank=True)# Use None for indefinite periods

    objects = OrganisationManager()

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return f"{self.code}|{self.name}"


class AccountManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Account(MP_Node):
    code = models.PositiveIntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    # level = models.PositiveIntegerField(db_index=True, default=0)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    posting = models.BooleanField(default=False)
    active_from = models.ForeignKey(FiscalYearPeriod, on_delete=models.PROTECT, related_name='account_active_from')
    active_to = models.ForeignKey(FiscalYearPeriod, on_delete=models.PROTECT, related_name='account_active_to', null=True, blank=True)# Use None for indefinite periods
    node_order_by = ['code']

    objects = AccountManager()

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return f"{self.code}|{self.name}"


class ProjectManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Project(MP_Node):
    code = models.PositiveIntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=186, unique=True)
    active_from = models.ForeignKey(FiscalYearPeriod, on_delete=models.PROTECT, related_name='project_active_from')
    active_to = models.ForeignKey(FiscalYearPeriod, on_delete=models.PROTECT, related_name='project_active_to', null=True, blank=True)# Use None for indefinite periods

    objects = ProjectManager()

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return f"{self.code}|{self.name}"


class FinancialDataManager(models.Manager):
    def get_by_natural_key(self, fiscal_year_period, organisation, account, project):
        return self.get(
            fiscal_year_period=fiscal_year_period,
            organisation=organisation,
            account=account,
            project=project
        )



class FinancialData(models.Model):
    fiscal_year_period = models.ForeignKey(
        FiscalYearPeriod,
        on_delete=models.PROTECT,
        db_index=True
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        db_index=True
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        db_index=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        db_index=True
    )
    actual = models.DecimalField(max_digits=15, decimal_places=2)
    working_forecast = models.DecimalField(
        max_digits=15, decimal_places=2,
        null=True, blank=True
    )
    original_budget = models.DecimalField(
        max_digits=15, decimal_places=2,
        null=True, blank=True
    )
    revised_budget = models.DecimalField(
        max_digits=15, decimal_places=2,
        null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'fiscal_year_period',
                    'organisation',
                    'account',
                    'project',
                ], name='unique_fiscal_year_period_organisation_account_project'
            )
        ]
        verbose_name_plural = "Financial Data"

    objects = FinancialDataManager()

    def natural_key(self):
        return (self.fiscal_year_period, self.organisation, self.account, self.project)

    def __str__(self):
        return f"FYP: {self.fiscal_year_period}, Org: {self.organisation}, Proj: {self.project}, Acc: {self.account}"
