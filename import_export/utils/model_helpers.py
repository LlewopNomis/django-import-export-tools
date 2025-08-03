import inspect
from django.db import models


def resolve_foreign_key(field, raw_value, choice_maps=None):
    related_model = field.remote_field.model

    if not isinstance(raw_value, (tuple, list)):
        raw_value = (raw_value,)

    if hasattr(related_model.objects, 'get_by_natural_key'):
        try:
            sig = inspect.signature(related_model.objects.get_by_natural_key)
            key_fields = list(sig.parameters.keys())
        except Exception:
            raise ValueError(f"Could not introspect natural_key() for {related_model.__name__}")
    else:
        raise ValueError(f"{related_model.__name__} must implement natural_key()")

    cleaned_key = []
    for i, key_part in enumerate(key_fields):
        rel_field = related_model._meta.get_field(key_part)
        value = raw_value[i]
        if choice_maps:
            if rel_field.choices:
                # Standard choices on this field
                source_model = rel_field.model.__name__
                model_choices = choice_maps.get(source_model, {}).get(key_part)
                if model_choices:
                    value = _map_choice_display_to_value(value, model_choices)
            elif rel_field.is_relation:
                # It's a ForeignKey — look deeper
                nested_model = rel_field.remote_field.model
                code_obj = nested_model.objects.get_by_natural_key.__code__
                nested_key_fields = list(code_obj.co_varnames[:code_obj.co_argcount])[1:]
                if len(nested_key_fields) == 1:
                    nested_key_field = nested_key_fields[0]
                    model_choices = choice_maps.get(nested_model.__name__, {}).get(nested_key_field)
                else:
                    raise NotImplementedError(
                        f"Compound nested natural keys are not yet supported for FK '{rel_field.name}': {nested_key_fields}"
                    )
                if model_choices:
                    value = _map_choice_display_to_value(value, model_choices)

        # 🔁 After all choice mapping — resolve FK object if needed
        if rel_field.is_relation and not isinstance(value, models.Model):
            nested_model = rel_field.remote_field.model
            try:
                if hasattr(nested_model.objects, 'get_by_natural_key'):
                    value = nested_model.objects.get_by_natural_key(value)
                else:
                    value = nested_model.objects.get(pk=value)
            except Exception as e:
                raise ValueError(f"Failed to resolve nested FK for {rel_field.name}: {value}. Error: {e}")

        # ✅ Final append
        cleaned_key.append(value)

    try:
        return related_model.objects.get_by_natural_key(*cleaned_key)
    except related_model.DoesNotExist:
        raise ValueError(f"{related_model.__name__} with natural key {cleaned_key} not found.")


def get_cleaned_field_value(field, raw_value, choice_maps=None):
    if field.choices and choice_maps:
        model_choices = choice_maps.get(field.model.__name__, {})
        if field.name in model_choices:
            return _map_choice_display_to_value(raw_value, model_choices[field.name])
    elif field.is_relation and (field.many_to_one or field.one_to_one):
        return resolve_foreign_key(field, raw_value, choice_maps)
    return raw_value


def _map_choice_display_to_value(display_value, choices_dict):
    try:
        return choices_dict[display_value]
    except KeyError:
        raise ValueError(f"Invalid choice '{display_value}'")
