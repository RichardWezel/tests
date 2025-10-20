from rest_framework import viewsets, generics, permissions
from forum_app.models import Like, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionThrottle, QuestionGetThrottle, QuestionPostThrottle
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .paginations import LargeResultsSetPagination, CustomLimitOffsetPagination


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'question-scope'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_throttles(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return [QuestionGetThrottle()]
            
    #     if self.action == 'create':
    #         return [QuestionPostThrottle()]
    
    #     return []














class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'content']
    search_fields = ['content', 'author__username']
    ordering_fields = ['content', 'author__username']
    ordering = ['content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     queryset = Answer.objects.all()

    #     content_param = self.request.query_params.get('content', None)
    #     if content_param is not None:
    #         queryset = queryset.filter(content__icontains=content_param)
    #     username_param = self.request.query_params.get('author', None)
    #     if username_param is not None:
    #         queryset = queryset.filter(author__username=username_param)
    #     question_id_param = self.request.query_params.get('question', None)
    #     if question_id_param is not None:
    #         queryset = queryset.filter(question__id=question_id_param)

    #     return queryset



class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]
    pagination_class = CustomLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
