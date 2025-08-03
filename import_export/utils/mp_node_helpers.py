MP_NODE_AUTO_FIELDS = {"path", "depth", "numchild"}

def create_mp_node(model, data):
    parent = data.pop('parent', None)
    try:
        lookup_key = model.objects.get_by_natural_key(*(model(**data).natural_key()))
        return lookup_key, False  # Already exists
    except model.DoesNotExist:
        if parent:
            return parent.add_child(**data), True
        else:
            return model.add_root(**data), True
