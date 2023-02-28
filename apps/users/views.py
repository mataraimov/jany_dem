import stripe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from rest_framework.response import Response
from django_filters import rest_framework as filterss
from rest_framework.reverse import reverse

from jany_dem import settings
from .forms import PostForm
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer,UserSerializer
from .models import Post
from django.contrib.auth import logout
from rest_framework import mixins, viewsets, renderers, pagination, status
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework_extensions.mixins import PaginateByMaxMixin
from django.views.generic import ListView
from rest_framework.decorators import action
stripe.api_key=settings.STRIPE_SECRET_KEY
class ProductFilter(filterss.FilterSet):
    min_target = filterss.NumberFilter(field_name="target", lookup_expr='gte')
    max_target = filterss.NumberFilter(field_name="target", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['target', 'balance']
class PaymentView(TemplateView):
    template_name = 'payment.html'

    def post(self, request, *args, **kwargs):
        amount = int(request.POST.get('amount', 0))
        token = request.POST.get('stripeToken')
        post_id = kwargs['pk']
        post = Post.objects.get(id=post_id)
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            description='Payment for post %s' % post_id,
            source=token,
        )
        post.update_balance(amount)
        return redirect(reverse('post-detail', args=[post.pk]))
class PostViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
        ListView
        ):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()

    serializer_class = PostSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    filter_backends = (filterss.DjangoFilterBackend,filters.SearchFilter)
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1
    search_fields = ['username', 'diagnose']
    model = Post
    post_queryset = Post.objects.all().order_by('target')
    template_name = 'update_post.html'
    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(username__icontains=query) |
                Q(diagnose__icontains=query) |
                Q(balance__icontains=query) |
                Q(target__icontains=query) |
                Q(treatment__icontains=query)
            )
        return qs
    def list(self, request, *args, **kwargs):
        response = super(PostViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data['results']}, template_name='posts.html')
        return response

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(user)
        return Response({'data': serializer.data}, template_name='profile.html')

    @action(detail=True, methods=['post'], name='Update Post')
    def update_post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect(reverse('post-detail', args=[post.pk]))  # update view name here
        else:
            initial_data = {
                'username': post.username,
                'age': post.age,
                'diagnose': post.diagnose,
                'treatment': post.treatment,
                'target': post.target,
                'description': post.description,
                'balance': post.balance,
            }
            form = PostForm(instance=post, initial=initial_data)
            print(form.target)

        return render(request, 'update_post.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


class MainView(TemplateView):
    template_name = "home.html"
class LoginView(LoginView):
    template_name = "login.html"