from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    param = request.GET.get('from-landing', '')
    if param == 'original':
        counter_click.update([param])
        # print("Клики", counter_click.most_common())
        return render(request, 'index.html')
    elif param == 'test':
        counter_click.update([param])
        # print("Клики", counter_click.most_common())
        return render(request, 'index.html')
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    param = request.GET.get('ab-test-arg', 'original')
    if param == 'original':
        counter_show.update([param])
        # print("Показы", counter_show.most_common())
        return render(request, 'landing.html')
    elif param == 'test':
        counter_show.update([param])
        # print("Показы", counter_show.most_common())
        return render(request, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        original_stats = counter_click['original']/counter_show['original']
        test_stats = counter_click['test']/counter_show['test']
        return render(request, 'stats.html', context={
            'original_conversion': original_stats,
            'test_conversion': test_stats,
        })
    except ZeroDivisionError:
        return render(request, 'stats.html', context={
            'original_conversion': f"Показы: {counter_show['original']} "
                                   f"Клики: {counter_click['original']}",
            'test_conversion': f"Показы: {counter_show['test']} "
                               f"Клики: {counter_click['test']}",
        })