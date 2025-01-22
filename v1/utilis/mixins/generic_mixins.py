from rest_framework import generics, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from v1.utilis.custom_responses import (
    serializer_without_paginator_res,
    success_response,
    serializer_error_response
)
from rest_framework import status


# Custom Mixins ====================================================================

class CustomCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = self.create_serializer_response()
        if response:
            return Response(serializer_without_paginator_res(serializer.data), status=status.HTTP_201_CREATED, headers=headers)
        return Response(success_response(), status=status.HTTP_201_CREATED, headers=headers)

    def create_serializer_response(self):
        pass


class CustomListModelMixin():
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer_without_paginator_res(serializer.data))


class CustomRetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer_without_paginator_res(serializer.data))


class CustomUpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(success_response())


class CustomDeleteModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(success_response())

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save()


# Custom GenericAPIView's============================================================

class CustomCreateAPIView(CustomCreateModelMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomListAPIView(CustomListModelMixin, generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class CustomRetrieveAPIView(CustomRetrieveModelMixin, generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CustomUpdateAPIView(CustomUpdateModelMixin, generics.GenericAPIView):
    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)


class CustomDeleteAPIView(CustomDeleteModelMixin, generics.GenericAPIView):
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# CustomViewSets
class CustomModelViewSet(
    CustomCreateModelMixin,
    CustomRetrieveModelMixin,
    CustomUpdateModelMixin,
    CustomDeleteModelMixin,
    CustomListModelMixin,
    GenericViewSet
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass