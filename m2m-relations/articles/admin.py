from django.contrib import admin
from .models import Article, Tag, Scope
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from pprint import pprint


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_quntity = 0
        for form in self.forms:
            # В form.cleaned_data - словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            # pprint(form.cleaned_data)
            if form.cleaned_data != {}:
                if form.cleaned_data['is_main'] == True:
                    is_main_quntity += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if is_main_quntity == 0:
            raise ValidationError('У статьи должен быть указан основной раздел')
        elif is_main_quntity > 1:
            raise ValidationError('У статьи должен быть указан только один основной раздел')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleTagInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image']
    list_display = ['published_at']
    inlines = [ArticleTagInline]


@admin.register(Tag)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name']
