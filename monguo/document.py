#!/usr/bin/env python
# @Author: lime
# @Date:   2013-10-25 19:45:09
# last modification by phil
# Date:<2017-11-24 05:00:27>

# todo : property caches

import inspect
import types
import motor
from bson.dbref import DBRef
from bson.objectid import ObjectId
from tornado.gen import coroutine, Return
from . import util
from .connection import Connection
from .error import *
from .field import *
from .validator import Validator

# insert_one and update_one do autodate
from datetime import datetime
from pymongo import DESCENDING
from pymongo.collection import Collection

__all__ = ['BaseDocument', 'EmbeddedDocument', 'Document']


class MonguoOperation(object):
    '''
    The query operation.

    Each one corresponds to the same name method of motor.
    '''

    def bound_method(self, monguo_method):
        '''
        Bound monguo method to motor method.

        :Parameters:
          - `monguo_method`: The method to be bounded.
        '''

        @classmethod
        def method(cls, *args, **kwargs):

            collection = cls.get_collection()
            motor_method = getattr(collection, monguo_method)

            validator = Validator(cls, collection)

            try:
                validate_method = getattr(validator, monguo_method)
                args, kwargs = validate_method(*args, **kwargs)
            except AttributeError:
                pass

            return motor_method(*args, **kwargs)

        return method


class MonguoMeta(type):
    '''Meta class of Document.'''

    def __new__(cls, name, bases, attrs):
        new_class = type.__new__(cls, name, bases, attrs)
        for base in reversed(inspect.getmro(new_class)):
            for name, attr in list(base.__dict__.items()):
                if isinstance(attr, Field):
                    if not util.legal_variable_name(name):
                        raise FieldNameError(field=name)

                elif isinstance(attr, MonguoOperation):
                    new_attr = attr.bound_method(name)
                    setattr(new_class, name, new_attr)

                elif isinstance(attr, types.FunctionType):
                    new_attr = staticmethod(attr)
                    setattr(new_class, name, new_attr)

        return new_class

class BaseDocument(object):
    '''The document base, not support query operations.'''

    @classmethod
    def fields_dict(cls):
        '''Get all the Field instance attributes.'''

        fields = {}
        for name, attr in list(cls.__dict__.items()):
            if isinstance(attr, Field):
                fields.update({name: attr})
        return fields

    @classmethod
    def validate_document(cls, document):
        '''Validate the given document.

        :Parameters:
          - `document`: The document to be validated.
        '''
        if not isinstance(document, dict):
            raise TypeError("Argument 'document' should be dict type.")

        _document = {}
        fields_dict = cls.fields_dict()

        for name, attr in list(document.items()):
            if not util.legal_variable_name(name):
                raise NameError("%s named error." % name)

            if name not in fields_dict:
                raise UndefinedFieldError(field=name)

        for name, attr in list(fields_dict.items()):
            if (attr.required and
                    name not in document and
                    attr.default is None ):
                raise RequiredError(field=name)

            value = None
            if (attr.required and
                    name not in document and
                    attr.default is not None):
                value = attr.default

            elif name in document:
                value = document[name]

            if value is not None:
                if not isinstance(attr, DictField):
                    value = attr.validate(value)
                else:
                    value = attr.document.validate_document(value)
                _document[name] = value

        return _document

class EmbeddedDocument(BaseDocument):
    '''The embedded document, not support query operations.'''
    pass


class Document(BaseDocument, metaclass=MonguoMeta):
    '''
    The ORM core, supports `all the query operations of motor
    <http://motor.readthedocs.org/en/stable/api/motor_collection.html>`_.'''
    meta              = {}

    create_index      = MonguoOperation()
    drop_indexes      = MonguoOperation()
    drop_index        = MonguoOperation()
    drop              = MonguoOperation()
    ensure_index      = MonguoOperation()
    reindex           = MonguoOperation()
    rename            = MonguoOperation()
    find_and_modify   = MonguoOperation()
    map_reduce        = MonguoOperation()
    update            = MonguoOperation()
    insert            = MonguoOperation()
    remove            = MonguoOperation()
    save              = MonguoOperation()
    index_information = MonguoOperation()
    count             = MonguoOperation()
    options           = MonguoOperation()
    group             = MonguoOperation()
    distinct          = MonguoOperation()
    inline_map_reduce = MonguoOperation()
    find_one          = MonguoOperation()
    find              = MonguoOperation()
    aggregate         = MonguoOperation()
    uuid_subtype      = MonguoOperation()
    full_name         = MonguoOperation()

    @classmethod
    def get_database_name(cls):
        '''Get the database name related to `cls`.'''
        db_name = (cls.meta['db'] if 'db' in cls.meta
                    else Connection.get_default_database_name())
        return db_name

    @classmethod
    def get_collection_name(cls):
        '''Get the collection name related to `cls`.'''

        collection_name = (cls.meta['collection'] if 'collection' in cls.meta
                            else util.camel_to_underline(cls.__name__))
        return collection_name

    @classmethod
    def get_database(cls, pymongo=False):
        '''
        Get the database related to `cls`, it's an instance of
        :class:`~motor.MotorDatabase`.

        :Parameters:
          - `pymongo`: Return pymongo.database if True.
        '''

        connection_name = cls.meta['connection'] if 'connection' in cls.meta else None
        db_name = cls.get_database_name()
        db = Connection.get_database(connection_name, db_name, pymongo)
        return db

    @classmethod
    def get_collection(cls, pymongo=False):
        '''
        Get the collection related to `cls`, it's an instance of
        :class:`~motor.MotorCollection`.

        :Parameters:
          - `pymongo`: Return pymongo.collection if True.
        '''

        db = cls.get_database(pymongo)
        collection_name = cls.get_collection_name()
        collection = db[collection_name]
        return collection


    @classmethod
    async def find_by_id(cls, _id):
        '''Get a document by id.

        :Parameters:
          - `id`:
        '''
        if not isinstance(dbref, DBRef):
            raise TypeError("'%s' isn't DBRef type." % dbref)

        if dbref.database:
            connection_name = cls.meta['connection'] if 'connection' in cls.meta else None
            db = Connection.get_database(connection_name, dbref.database)
        else:
            db = cls.get_database()

        collection = db[dbref.collection]
        result = await collection.find_one({'_id': ObjectId(_id)})
        return result

    @classmethod
    async def get_embed_ref(cls, dbref, fields=None):
        '''Get the document related with `dbref`.

        :Parameters:
          - `dbref`: The dbref to be translated.
        '''
        if not isinstance(dbref, DBRef):
            raise TypeError("'%s' isn't DBRef type." % dbref)

        if dbref.database :
            connection_name = cls.meta['connection'] if 'connection' in cls.meta else None
            db = Connection.get_database(connection_name, dbref.database)
        else:
            db = cls.get_database()

        collection = db[dbref.collection]
        result = await collection.find_one({'_id': ObjectId(dbref.id)}, fields)
        return result

    @classmethod
    async def embed_refs(cls, document, depth=1):
        '''Translate all dbrefs in the specified `document`.

        :Parameters:
          - `document`: The specified document.
          - `depth`: The translate depth.
        '''
        if not isinstance(document, dict):
            raise TypeError("Argument 'document' should be dict type.")

        for name, value in list(document.items()):
            if isinstance(value, DBRef):
                document[name] = await cls.get_embed_ref(value)
                if depth > 1:
                    document[name] = await cls.embed_refs(
                        document[name], depth - 1)

        return document


    @classmethod
    async def embed_ref_in_doclist(cls, doc_list, depth=1):
        '''Translate dbrefs in the document list.

        :Parameters:
          - `document_list`: The specified document list.
          - `depth`: The translate depth.
        '''
        if not isinstance(doc_list, (list, tuple)):
            raise TypeError("Argument document_list should be list or tuple tpye.")

        for document in doc_list:
            document = await cls.embed_refs(document, depth)

        return document_list

    @classmethod
    @coroutine
    def to_list(cls, cursor, length=None):
        '''Warp cursor.to_list() since `length` is required in `cursor.to_list`'''

        res = []

        if length is not None:
            assert isinstance(length, int)
            res = yield cursor.to_list(length=length)
        else:
            while (yield cursor.fetch_next):
                res.append(cursor.next_object())

        raise Return(res)

    @classmethod
    @coroutine
    def list( cls, filtr={},
                        page=0,
                        pageSize=10,
                        sort='date',
                        order=DESCENDING) :
        skip = page * pageSize
        cursor = cls.find(filtr).sort([(sort, order)]).skip(skip).limit(pageSize)
        c = yield cls.to_list(cursor)
        raise Return(c)

    @classmethod
    async def delete_list(cls,oids):
        doclist = [ObjectId(oid) for oid in oids]
        r = await cls.remove({'_id': {'$in':doclist}})
        return r

    @classmethod
    async def insert_one(cls,doc):
        doc.update({'date':datetime.now()})
        return cls.insert(doc)


    @classmethod
    async def update_one(cls,id,doc):
        doc.update({'update':datetime.now()})
        return cls.update(
            {'_id': ObjectId(id)},
            {'$set': doc}
        )

    @classmethod
    def find_one_sync(cls,_id):
        return cls.get_collection(pymongo=True).find_one({'_id': ObjectId(_id)})

    @classmethod
    def get_gridfs(cls, async=True):
        if async:
            db = Connection.get_database()
            fs = motor.MotorGridFS(db)
        else:
            db = Connection.get_database(pymongo=True)
            fs = gridfs.GridFS(db)

        return fs



    @classmethod
    async def archive_list(Cls,oids):
        ''' need to archive the post as well '''
        oids = [ObjectId(oid) for oid in oids]
        S = Cls.get_collection(pymongo=True)
        D = Cls.get_database(pymongo=True)
        try:
            T = Collection(D,Cls.__name__+'_archives',create=True)
        except Exception : # OperationFailure
            T = Collection(D,Cls.__name__+'_archives')
        bulkInsert = T.initialize_unordered_bulk_op()
        bulkRemove = S.initialize_unordered_bulk_op()

        docs = list(S.find({"_id":{'$in': oids}}))
        x = 1000
        counter = 0

        for doc in docs :
            bulkInsert.insert(doc)
            bulkRemove.find({'_id':doc['_id']}).remove_one()
            counter += 1
            if counter % x == 0 :
                bulkInsert.execute()
                bulkRemove.execute()
                bulkInsert = T.initialize_unordered_bulk_op()
                bulkRemove = S.initialize_unordered_bulk_op()

        bulkInsert.execute()
        bulkRemove.execute()


class AutoDateDocument(Document, metaclass=MonguoMeta):
    @classmethod
    async def insert_one(cls,id,doc):
        doc.update({'date':datetime.now()})
        return cls.update(
            {'_id': ObjectId(id)},
            {'$set': doc}
        )

    @classmethod
    async def update_one(cls,id,doc):
        doc.update({'update':datetime.now()})
        return cls.update(
            {'_id': ObjectId(id)},
            {'$set': doc}
        )
