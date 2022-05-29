from rest_framework import generics as api_views, permissions

from djangoRestWorkshop.todos.models import Todo, Category
from djangoRestWorkshop.todos.serializers import TodoForListSerializer, CategoryForListSerializer, \
    TodoSerializer


class TodosListOrCreateView(api_views.ListCreateAPIView):
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    list_serializer_class = TodoForListSerializer
    create_serializer_class = TodoSerializer
    query_filter_names = ('category',)

    # filter func
    def __apply_query_filters(self, queryset):
        filter_options = {}

        for filter_name in self.query_filter_names:
            id = self.request.query_params.get(filter_name, None)
            if id:
                filter_options[f'{filter_name}_id'] = id

        return queryset.filter(**filter_options)

    def get_queryset(self):
        queryset = super().get_queryset()

        # show only user's todos
        queryset = queryset.filter(user=self.request.user)

        # show filtered todos
        queryset = self.__apply_query_filters(queryset)

        return queryset

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.list_serializer_class


class TodosUpdateAndDetailsView(api_views.RetrieveUpdateAPIView):
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer


class CategoryListView(api_views.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryForListSerializer

    # show only categories containing user's todos
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(todo__user=self.request.user)
    #     return queryset
