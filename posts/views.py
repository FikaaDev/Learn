from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

# making custom pagination.
class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page"
    page_size_query_param = "page_size"

@api_view(http_method_names=["GET","POST"])
# "IsAuthenticated" for having a valid authentication to hit the api
# @permission_classes([IsAuthenticated])
# "AllowAny" allow anyone to hit the api
@permission_classes([AllowAny])
# "IsAuthenticatedOrReadOnly" allow anyone to get but only post with authetication.
# @permission_classes([IsAuthenticatedOrReadOnly])
# "IsAdminUser" allow only an admin user to hit the api
# @permission_classes([IsAdminUser])
def homepage(request:Request):
    if (request.method == "POST"):
        data = request.data
        response = {"Message": "Hello", "data":data}
        return Response(data=response, status=status.HTTP_201_CREATED)
    
    if (request.method == "GET"):
        response = {"Message": "Hello"}
        return Response(data=response, status=status.HTTP_200_OK)
    
    
@api_view(http_method_names=["GET"])
@permission_classes([])
def get_post_by_id(request:Request, post_index: int):
    post = get_object_or_404(Post, pk=post_index)

    serializer = PostSerializer(instance=post)
    response = {
                "Message": "Post fetched",
                "data_inserted": serializer.data
    }
    return Response(data = response, status=status.HTTP_200_OK)

@api_view(http_method_names=["GET","POST"])
@permission_classes([])
def list_posts(request: Request):
    if(request.method == "POST"):
        user_data = request.data
        # "data" will be the user given object
        serializer = PostSerializer(data = user_data)

        if (serializer.is_valid()):
            serializer.save()
            response = {
                "Message": "Post Created",
                "data_inserted": serializer.data
            }

            return Response(data = response, status=status.HTTP_201_CREATED)
        
        return Response(data = serializer.error_messages, status= status.HTTP_400_BAD_REQUEST)
    
 
    if (request.method == "GET"):
        # Fetch everything from DB model object "Post"    
        post = Post.objects.all()
        # Initialize Serializer
        # mention the data you want to return as a JSON Onject inside the serializer
        # "instance" will be what you want to be JSONised
        serializer = PostSerializer(instance = post, many = True)
        response = {"Message": "Post", "post_index":serializer.data}
        # "serializer.data" helps us get JSON format of the object
        return Response(data = response, status=status.HTTP_200_OK)

@api_view(http_method_names=["PUT"])
@permission_classes([])
def update_post_by_id(request:Request, post_index: int):
    post = get_object_or_404(Post, pk=post_index)
    data = request.data
    # "instance" will be what you want to update and "data" will be the updated user given object. 
    serializer = PostSerializer(instance = post, data = data)
    if (serializer.is_valid()):
        serializer.save()
        response = {"Message": "Successfully Updated", 
                    "data_updated":serializer.data}
        
        return Response(data = response, status= status.HTTP_200_OK)
    return Response(data = serializer.error_messages, status= status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=["DELETE"])
@permission_classes([])
def delete_post_by_id(request:Request, post_index: int):
    post = get_object_or_404(Post, pk=post_index)
    post.delete()
    return Response(status= status.HTTP_204_NO_CONTENT)

# ===================== Class Method ==============================

class PostListCreateView(APIView):

    """
        A view for listing and posting
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, *args, **kwargs):
        posts = Post.objects.all()
        #  many = True will return all the values in format of list of jsons.
        serializer = self.serializer_class(instance= posts, many= True)
        return Response(data  = serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request: Request, *args, **kwargs):
        user_data = request.data
        serializer = self.serializer_class(data = user_data)
        if (serializer.is_valid()):
            serializer.save()
            response = {"Message": "Successfully Updated", 
                        "data_updated":serializer.data}
            return Response(data = response, status= status.HTTP_200_OK)
        return Response(data = serializer.error_messages, status= status.HTTP_400_BAD_REQUEST)


class PostRetriveUpdateDeleteView(APIView):
    """
        A view for Retriving, Updating, Deleting posts by id
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, post_index: int):
        post = get_object_or_404(Post,pk=post_index)
        serializer = self.serializer_class(instance=post)
        return Response(data = serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request: Request, post_index: int):
        post = get_object_or_404(Post, pk=post_index)
        user_data = request.data
        serializer = self.serializer_class(instance=post, data = user_data)
        if (serializer.is_valid()):
            serializer.save()
            response = {"Message": "Successfully Updated", 
                        "data_updated":serializer.data}
            return Response(data = response, status= status.HTTP_200_OK)
        return Response(data = serializer.error_messages, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request:Request, post_index: int):
        post = get_object_or_404(Post, pk= post_index)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # ==================== using generics and mixins ==========================



class PostGenericListCreateView(generics.GenericAPIView, 
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin):
    """
        A view for listing and posting using Generics and Mixins
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    # perform_create(self, serializer) - Called by CreateModelMixin when saving a new object instance.
    # After the post => CreateModelMixin => perform_create() => over-ride and  adding behavior that occurs before or after saving an object.

    # self.create => creates the default post as per mentioned y the serialiser having values  
    # "id",
    # "title",
    # "content",
    # "created",
    # But we want to add the "author" as the "user" via the req. Hence we have added the "perform_create".

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    


class PostGenericRetriveUpdateDeleteView(generics.GenericAPIView,
                                         mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         mixins.DestroyModelMixin):
    """
        A view for Retriving, Updating, Deleting posts by id using generics and Mixin
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class ListPostsForAuthor(generics.GenericAPIView, 
                                mixins.ListModelMixin):
    
    queryset = Post.objects.all()
    serializer_class  = PostSerializer
    permission_classes = [IsAuthenticated]

    # "get_queryset" is for over riding the default get.
    def get_queryset(self):
        # How are we getting "user" in the request?
        user = self.request.user
        response = Post.objects.filter(author = user)
        return response

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ListPostsForAuthorQuery(generics.GenericAPIView, 
                                mixins.ListModelMixin):
    
    queryset = Post.objects.all()
    serializer_class  = PostSerializer
    permission_classes = [IsAuthenticated]

    # "get_queryset" is for over riding the default get.
    def get_queryset(self):
        # How are we getting "user" in the request?
        username = self.kwargs.get("user_name")
        response = Post.objects.filter(author__username = username)
        return response

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ListPostsForAuthorQueryParams(generics.GenericAPIView, 
                                mixins.ListModelMixin):
    
    queryset = Post.objects.all()
    serializer_class  = PostSerializer
    permission_classes = [IsAuthenticated]

    # "get_queryset" is for over riding the default get.
    def get_queryset(self):
        # How are we getting "user" in the request?
        username = self.request.query_params.get("user_name") or None
        queryset = Post.objects.all()
        if username is not None:
            return Post.objects.filter(author__username = username)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# =========================== View Sets ===========================
# View and routers
# Routers allow us to map a viewset onto our url. Viewsets 
class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request: Request):
        queryset = Post.objects.all()
        serializer = PostSerializer(instance=queryset, many = True)
        return Response(data = serializer.data, status= status.HTTP_200_OK)
    
    def retriev(self, request: Request, pk =  None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(instance=post, many = True)
        return Response(data = serializer.data, status= status.HTTP_200_OK)


# modelViewSet
class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


