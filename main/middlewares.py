from .models import SocialUser

def social_context_processor(request):
    context = {}
    context['all'] = ''
    pk = request.user.pk
    if pk:
        User = SocialUser.objects.get(pk=pk)
        count = User.message_set.filter(is_active=True)
        context['count'] = count
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context