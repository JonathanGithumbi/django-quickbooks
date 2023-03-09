import logging
from abc import ABC

from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.exceptions import QBObjectServiceNotImplemented
from django_quickbooks.exceptions import ValidationError
from django_quickbooks.objects import import_object_cls
from django_quickbooks.utils import xml_setter
from django_quickbooks.validators import SchemeValidator, is_primitive, is_list


def _default_value_setter(key, type):
    if type == 'LISTTYPE':
        return []
    return None


class BaseObject(ABC):
    fields = dict()
    validator = SchemeValidator()

    def __setattr__(self, key, value):
        if key in self.fields:
            super().__setattr__(key, value)

    def __init__(self, **kwargs):
        errors = []
        # FIXME: ValidationError handling still seems clumsy, need to reviewed
        for field_name, value in kwargs.items():
            try:
                self.validator.validate(
                    field_name, value, **self.fields[field_name])
                setattr(self, field_name, value)
            except ValidationError as exc:
                errors.append(exc.detail)

        if errors:
            logger = logging.getLogger('django.request')
            logging.error(errors)
            raise ValidationError(errors)

        for field_name, options in self.fields.items():
            if not hasattr(self, field_name):
                setattr(self,
                        field_name,
                        _default_value_setter(
                            field_name, self.fields[field_name]['validator']['type'])
                        )

    def as_xml(self, class_name=None, indent=0, opp_type=QUICKBOOKS_ENUMS.OPP_ADD,
               version=QUICKBOOKS_ENUMS.VERSION_13, **kwargs):
        """This code defines a method called as_xml which is a part of a class. The purpose of this method is to convert the object of the class into an XML format. The method takes a few arguments like class_name, indent, opp_type, version, and some additional keyword arguments.

The method first initializes an empty string called xml which will later contain the XML representation of the object. It then iterates over each field of the object using a for loop. For each field, it checks if the object has the attribute corresponding to that field. If not, it skips that field.

If the field contains a primitive value, the method converts the value into a string and adds an XML element to xml using the xml_setter function. This function sets the XML element with the name of the field and the string representation of the value. If the field is a boolean, the string representation of the value is converted to lowercase.

If the field contains a list of elements, the method iterates over each element in the list. If the element is a primitive value, the method follows the same process as before to add an XML element to xml. If the element is an object, the method recursively calls the as_xml method of that object with some modified arguments based on the type of the field. If the field is a reference field, the object's as_xml method is called with the OBJ_REF type of operation. If the field is a change field, the object's as_xml method is called with the opp_type argument that was passed to the method. If the field is a complex field, the object's as_xml method is called with an empty opp_type argument.

If the field contains an object, the method follows the same process as when the element of a list is an object, but the arguments passed to the as_xml method are determined based on the type of the field.

Finally, the class_name, opp_type, and xml are used to create the final XML representation of the object. The class_name and opp_type are combined to create the root element of the XML, and the xml variable contains the XML elements for all the fields of the object. These are then combined using the xml_setter function and returned as the final XML output."""
        xml = ''
        #
        for field_key, options in self.fields.items():
            if hasattr(self, field_key):
                obj = getattr(self, field_key)
                if not obj:
                    continue
                if is_primitive(obj):
                    if self.fields[field_key]['validator']['type'] == self.validator.BOOLTYPE:
                        xml += xml_setter(field_key,
                                          str(obj).lower(), encode=True)
                    else:
                        xml += xml_setter(field_key, str(obj), encode=True)

                elif is_list(obj):
                    for element in obj:
                        if is_primitive(element):
                            if self.fields[field_key]['validator']['type'] == self.validator.BOOLTYPE:
                                xml += xml_setter(field_key,
                                                  str(element).lower(), encode=True)
                            else:
                                xml += xml_setter(field_key,
                                                  str(element), encode=True)
                        else:
                            if field_key in kwargs.get('ref_fields', []):
                                xml += element.as_xml(class_name=field_key, indent=indent,
                                                      opp_type=QUICKBOOKS_ENUMS.OBJ_REF, version=version, **kwargs)
                            elif field_key in kwargs.get('change_fields', []):
                                xml += element.as_xml(class_name=field_key, indent=indent, opp_type=opp_type,
                                                      version=version, **kwargs)
                            elif field_key in kwargs.get('complex_fields', []):
                                xml += element.as_xml(class_name=field_key, indent=indent, opp_type='', version=version,
                                                      **kwargs)
                else:
                    if field_key in kwargs.get('ref_fields', []):
                        xml += obj.as_xml(class_name=field_key, indent=indent, opp_type=QUICKBOOKS_ENUMS.OBJ_REF,
                                          version=version, **kwargs)
                    elif field_key in kwargs.get('change_fields', []):
                        xml += obj.as_xml(class_name=field_key, indent=indent, opp_type=opp_type, version=version,
                                          **kwargs)
                    elif field_key in kwargs.get('complex_fields', []):
                        xml += obj.as_xml(class_name=field_key, indent=indent,
                                          opp_type='', version=version, **kwargs)

        class_name = self.__class__.__name__ if not class_name else class_name
        xml = xml_setter(class_name + opp_type, xml)
        return xml

    @classmethod
    def from_lxml(cls, lxml_obj):

        def to_internal_value(field, type):
            converters = dict(
                STRTYPE=lambda x: x.text,
                ESTYPE=lambda x: x.text,
                IDTYPE=lambda x: x.text,
                FLOATTYPE=lambda x: float(x.text),
                BOOLTYPE=lambda x: bool(x.text),
                OBJTYPE=lambda x: import_object_cls(x.tag).from_lxml(x),
            )
            return converters[type](field) if type in converters else None

        obj_data = dict()
        for field in list(lxml_obj):
            field_name = field.tag
            value = None
            if field_name in cls.fields:
                value = to_internal_value(
                    field, cls.fields[field_name]['validator']['type'])
            elif field_name == 'ParentRef':
                field_name = 'Parent'
                value = cls.from_lxml(field)
            elif isinstance(field_name, str) and any(
                    index == len(field_name) - 3 for index in list(map(field_name.find, ['Ref', 'Ret']))):
                field_name = field_name[:len(field_name) - 3]
                if field_name in cls.fields:
                    field.tag = field_name
                    value = to_internal_value(
                        field, cls.fields[field_name]['validator']['type'])
            if value:
                if field_name in cls.fields and cls.fields[field_name].get('many', False):
                    if field_name in obj_data:
                        obj_data[field_name].append(value)
                    else:
                        obj_data[field_name] = [value]
                else:
                    obj_data[field_name] = value

        return cls(**obj_data)

    def __eq__(self, other):
        for field_name, options in self.fields.items():
            if not hasattr(self, field_name) and hasattr(other, field_name):
                return False
            if not hasattr(other, field_name) and hasattr(self, field_name):
                return False
            if getattr(self, field_name) != getattr(other, field_name):
                return False
        return True

    @staticmethod
    def get_service():
        raise QBObjectServiceNotImplemented
