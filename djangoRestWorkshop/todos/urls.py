from django.urls import path

from djangoRestWorkshop.todos.views import TodosListOrCreateView, CategoryListView, TodosUpdateAndDetailsView

urlpatterns = [
    path('', TodosListOrCreateView.as_view(), name='todo list or create'),
    path('categories/', CategoryListView.as_view(), name='category list'),
    path('<int:pk>/', TodosUpdateAndDetailsView.as_view(), name='todo update or detail'),
]
