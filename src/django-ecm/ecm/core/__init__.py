# -*- coding: utf-8 -*-

class TypeRegistry:
    """
    Register Class for ECM content types
    """
    models = []

    def register(self, model):
        if model not in self.models:
            self.models.append(model)

toc = TypeRegistry()
