# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .base import _BlankMixin, _BaseAmoManager, _Helper
from .utils import lazy_dict_property

import six

__all__ = ['AmoApi', 'NotesManager', 'ContactsManager', 'CompanyManager', 'LeadsManager', 'TasksManager']


class ContactsManager(_BlankMixin, _BaseAmoManager):
    name = 'contacts'
    _main_field = 'name'
    _object_type = 'contact'

    def _add_data(self, **kwargs):
        kwargs.setdefault('responsible_user_id', self.user.id)
        return super(ContactsManager, self)._add_data(**kwargs)


class CompanyManager(_BlankMixin, _BaseAmoManager):
    name = 'company'
    _container_name = 'contacts'
    _object_type = name
    _main_field = 'name'

    @lazy_dict_property
    def _custom_fields(self):
        return self.get_custom_fields(to='companies')


class LeadsManager(_BlankMixin, _BaseAmoManager):
    name = 'leads'

    def all(self, query=None, status=None, **kwargs):
        query = query or {}
        if status:
            if not ((isinstance(status, six.string_types) and status.isdigit()) or isinstance(status, int)):
                status = self.leads_statuses[status]['id']
            query['status'] = status
        return super(LeadsManager, self).all(query=query, **kwargs)


class _ObjectIdMixin(object):
    def __init__(self, object_type=None, *args, **kwargs):
        super(_ObjectIdMixin, self).__init__(*args, **kwargs)
        self._object_type = object_type


class TasksManager(_ObjectIdMixin, _BlankMixin, _BaseAmoManager):
    name = 'tasks'
    _main_field = 'element_id'

    def search(self, *args, **kwargs):
        raise Exception('Amocrm havn\'t task search ability ')

    def _create_or_update_data(self, **data):
        return self.add(**data)


class NotesManager(_ObjectIdMixin, _BlankMixin, _BaseAmoManager):
    name = 'notes'
    _main_field = 'element_id'

    def search(self, *args, **kwargs):
        raise Exception('Amocrm havn\'t note search ability ')

    def _create_or_update_data(self, **data):
        return self.add(**data)


class AmoApi(_Helper(ContactsManager, 'contacts'), _Helper(CompanyManager, 'company'),
             _Helper(NotesManager, 'notes'), _Helper(LeadsManager, 'leads'), _Helper(TasksManager, 'tasks'),
             _BlankMixin, _BaseAmoManager):
    name = 'accounts'

