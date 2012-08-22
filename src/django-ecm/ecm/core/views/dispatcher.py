# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.utils.decorators import classonlymethod
from django.utils.functional import update_wrapper

from django.contrib.contenttypes.models import ContentType

from ecm.core.models import ECMCatalog


class ECMView(View):
    context_key = 'slugs'
    action = None

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(u"You tried to pass in the %s method name as a "
                                u"keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError(u"%s() received an invalid keyword %r" % (
                    cls.__name__, key))

        def get_slugs(**kwargs):
            """
            Return slugs context from URL.
            """
            return kwargs.get(cls.context_key).split('/')

        def get_traversal(**kwargs):
            """
            Get traversal (catalog entry) from URL.
            """
            slugs = get_slugs(**kwargs)
            unordered_brains = ECMCatalog.objects.filter(slug__in=slugs)
            d = {}
            for b in unordered_brains:
                d[b.slug] = b
            ordered_brains = []
            for s in slugs:
                ordered_brains.append(d[s])
            return ordered_brains

        def view(request, *args, **kwargs):
            """
            Lookup the view class and return an instance of.
            """
            # Setup the context
            traversal = get_traversal(**kwargs)
            node = traversal[-1].get_object()

            # Check if content type is not determined by view
            ct = kwargs.get('content_type', None)
            if ct is None:
                content_type = node.content_type
            else:
                content_type = ContentType.objects.get(model=ct.lower())
            model_class = content_type.model_class()

            # Goof stuff to make available in views
            kwargs.update({
                'traversal': traversal,
                'node': node,
                'model': model_class,
                })

            # Do check in model for considered content to
            # find to good view URL( action) / content type / content id
            action = initkwargs.get('action', None)
            model_view_attr = "%s_view" % action 
            view_name = getattr(node, model_view_attr, None)
            if hasattr(view_name, '__call__'):
                view_name = view_name(request, *args, **kwargs)
            if action is None or view_name is None:
                raise Exception("ECM View must have an 'action' "
                        "parameter which map on 'action_view' property "
                        "of content.")
            path = view_name.split('.')
            klass = path.pop()
            module = __import__(".".join(path), fromlist=".")
            view = getattr(module, klass)

            self = view(**initkwargs)
            self.model = model_class
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view
