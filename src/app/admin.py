from django.contrib import admin 
from django.contrib.admin import AdminSite
from app.models import *
from django.utils.translation import gettext_lazy
from import_export.admin import ExportActionModelAdmin
from import_export import resources
# Register your models here.
admin.site.register(MehrUser)
admin.site.register(Project)
admin.site.register(Institute)
# admin_site.register(OtpUser)


# admin.site.register(AuthUser)
@admin.action(description='نهایی کردن پرداخت')
def PayHelp(modeladmin,request,queryset):
    for item in queryset:
        if item.state == State.paynext and item.expiration > 1 :
            CharityHelp.objects.create(user = item.user,project = item.project , price = item.price,expiration=item.expiration -1)
            queryset.update(state = State.success)
        elif item.state == State.paynext and item.expiration == 1 :
            CharityHelp.objects.create(state = State.expired,user = item.user,project = item.project , price = item.price,expiration=item.expiration -1)
            queryset.update(state = State.success)


class ExportResorce(resources.ModelResource):

    class Meta:
        model = CharityHelp
        fields = ('user__firstName','user__lastName','project__topic','project__institute__name','price')
        export_order = ('user__firstName','user__lastName','project__topic','project__institute__name','price')



@admin.action(description='گزارش خروجی')
class ExportAdmin(ExportActionModelAdmin):    
    resource_classes = [ExportResorce]


from django.contrib import admin

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class CustomDateFilter(admin.SimpleListFilter):
    title = gettext_lazy('تاریخ')
    parameter_name = 'تاریخ'

    def lookups(self, request, model_admin):
        # define the filter options
        return (
            # ('all',gettext_lazy('همه')),
            ('this month', gettext_lazy('این ماه')),
            ('last month', gettext_lazy('ماه قبل')),
        )

    def queryset(self, request, queryset):
        # apply the filter to the queryset
        if self.value() == 'this month':
            thisMonth = datetime.now().month
            queryset = CharityHelp.objects.filter(date__month__exact = thisMonth)
            return queryset
        if self.value() == 'last month':
            lastmonth = datetime.now().month - 1
            queryset = CharityHelp.objects.filter(date__month__exact = lastmonth)
            return queryset
        # if self.value() == 'all':
        #     queryset = CharityHelp.objects.all()
        #     return queryset    

class UserHelpPayment(ExportAdmin,admin.ModelAdmin):
    actions = [PayHelp]
    search_fields = ['project__topic']
    list_filter = (
        ("project",custom_titled_filter("پروژه")),
        ("user",custom_titled_filter("کاربر")),
        # ("date",custom_titled_filter("تاریخ")),
        (CustomDateFilter)
    )

    
admin.site.register(CharityHelp,UserHelpPayment)


# class MehrAdminSite(AdminSite):
#     site_title = gettext_lazy("ادمین  دیجی کالا مهر")
#     site_header = gettext_lazy("ادمین  دیجی کالا مهر")



# admin0site = MehrAdminSite()



