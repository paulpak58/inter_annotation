# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data_interface/sages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='data_interface/sages.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1a\x64\x61ta_interface/sages.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"O\n\x0eSurgicalObject\x12\x13\n\x0bobject_name\x18\x01 \x01(\t\x12\x14\n\x0cobject_value\x18\x02 \x01(\t\x12\x12\n\nobject_uid\x18\x03 \x01(\t\"9\n\x0e\x45xternalEntity\x12\x13\n\x0b\x65ntity_name\x18\x01 \x01(\t\x12\x12\n\nentity_uid\x18\x02 \x01(\t\"\x8e\x01\n\x10TemporalInterval\x12)\n\x05start\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x03\x65nd\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bstart_exact\x18\x03 \x01(\x08\x12\x11\n\tend_exact\x18\x04 \x01(\x08\"O\n\rTemporalPoint\x12)\n\x05point\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bpoint_exact\x18\x02 \x01(\x08\"$\n\x0c\x43oordinate2D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\".\n\x0bSpatialSpan\x12\x1f\n\x08\x65lements\x18\x01 \x03(\x0b\x32\r.Coordinate2D\"\xfa\x01\n\x05\x45vent\x12\x0f\n\x07\x63omment\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12.\n\x11temporal_interval\x18\x03 \x01(\x0b\x32\x11.TemporalIntervalH\x00\x12(\n\x0etemporal_point\x18\x04 \x01(\x0b\x32\x0e.TemporalPointH\x00\x12\x1b\n\x11temporal_constant\x18\x05 \x01(\x08H\x00\x12\"\n\x0cspatial_span\x18\x06 \x01(\x0b\x32\x0c.SpatialSpan\x12\x10\n\x08video_id\x18\x07 \x01(\t\x12\x14\n\x0c\x61nnotator_id\x18\x08 \x01(\tB\x0f\n\rtemporal_span\"\x92\x01\n\rSurgeryEntity\x12\x17\n\x05\x65vent\x18\x01 \x01(\x0b\x32\x06.EventH\x00\x12!\n\x06object\x18\x02 \x01(\x0b\x32\x0f.SurgicalObjectH\x00\x12*\n\x0f\x65xternal_entity\x18\x03 \x01(\x0b\x32\x0f.ExternalEntityH\x00\x12\x11\n\tentity_id\x18\x04 \x01(\tB\x06\n\x04type\"7\n\x05Track\x12\x0c\n\x04name\x18\x01 \x01(\t\x12 \n\x08\x65ntities\x18\x02 \x03(\x0b\x32\x0e.SurgeryEntity\"3\n\x0bTracksGroup\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x16\n\x06tracks\x18\x02 \x03(\x0b\x32\x06.Track\"\xb0\x01\n\x08Relation\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x12\n\nentity_ids\x18\x02 \x03(\t\x12\x44\n\x16\x61\x64\x64itional_information\x18\x03 \x03(\x0b\x32$.Relation.AdditionalInformationEntry\x1a<\n\x1a\x41\x64\x64itionalInformationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"o\n\rAnnotationSet\x12#\n\rtracks_groups\x18\x01 \x03(\x0b\x32\x0c.TracksGroup\x12%\n\x12temporal_relations\x18\x02 \x03(\x0b\x32\t.Relation\x12\x12\n\nsurgery_id\x18\x03 \x01(\t\"\x8c\x01\n\x19\x41nnotationModelDefinition\x12%\n\x0c\x65ntity_types\x18\x01 \x03(\x0b\x32\x0f.SurgicalObject\x12\x1e\n\x0b\x63onstraints\x18\x02 \x03(\x0b\x32\t.Relation\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x17\n\x0finstructions_id\x18\x04 \x01(\tb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_SURGICALOBJECT = _descriptor.Descriptor(
  name='SurgicalObject',
  full_name='SurgicalObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='object_name', full_name='SurgicalObject.object_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object_value', full_name='SurgicalObject.object_value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object_uid', full_name='SurgicalObject.object_uid', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=63,
  serialized_end=142,
)


_EXTERNALENTITY = _descriptor.Descriptor(
  name='ExternalEntity',
  full_name='ExternalEntity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity_name', full_name='ExternalEntity.entity_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entity_uid', full_name='ExternalEntity.entity_uid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=201,
)


_TEMPORALINTERVAL = _descriptor.Descriptor(
  name='TemporalInterval',
  full_name='TemporalInterval',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='TemporalInterval.start', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='TemporalInterval.end', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_exact', full_name='TemporalInterval.start_exact', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end_exact', full_name='TemporalInterval.end_exact', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=204,
  serialized_end=346,
)


_TEMPORALPOINT = _descriptor.Descriptor(
  name='TemporalPoint',
  full_name='TemporalPoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='point', full_name='TemporalPoint.point', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='point_exact', full_name='TemporalPoint.point_exact', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=348,
  serialized_end=427,
)


_COORDINATE2D = _descriptor.Descriptor(
  name='Coordinate2D',
  full_name='Coordinate2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Coordinate2D.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='Coordinate2D.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=429,
  serialized_end=465,
)


_SPATIALSPAN = _descriptor.Descriptor(
  name='SpatialSpan',
  full_name='SpatialSpan',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elements', full_name='SpatialSpan.elements', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=467,
  serialized_end=513,
)


_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='comment', full_name='Event.comment', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='Event.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temporal_interval', full_name='Event.temporal_interval', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temporal_point', full_name='Event.temporal_point', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temporal_constant', full_name='Event.temporal_constant', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='spatial_span', full_name='Event.spatial_span', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='video_id', full_name='Event.video_id', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='annotator_id', full_name='Event.annotator_id', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='temporal_span', full_name='Event.temporal_span',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=516,
  serialized_end=766,
)


_SURGERYENTITY = _descriptor.Descriptor(
  name='SurgeryEntity',
  full_name='SurgeryEntity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='event', full_name='SurgeryEntity.event', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object', full_name='SurgeryEntity.object', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='external_entity', full_name='SurgeryEntity.external_entity', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entity_id', full_name='SurgeryEntity.entity_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type', full_name='SurgeryEntity.type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=769,
  serialized_end=915,
)


_TRACK = _descriptor.Descriptor(
  name='Track',
  full_name='Track',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Track.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entities', full_name='Track.entities', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=917,
  serialized_end=972,
)


_TRACKSGROUP = _descriptor.Descriptor(
  name='TracksGroup',
  full_name='TracksGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='TracksGroup.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tracks', full_name='TracksGroup.tracks', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=974,
  serialized_end=1025,
)


_RELATION_ADDITIONALINFORMATIONENTRY = _descriptor.Descriptor(
  name='AdditionalInformationEntry',
  full_name='Relation.AdditionalInformationEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Relation.AdditionalInformationEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='Relation.AdditionalInformationEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1144,
  serialized_end=1204,
)

_RELATION = _descriptor.Descriptor(
  name='Relation',
  full_name='Relation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Relation.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entity_ids', full_name='Relation.entity_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='additional_information', full_name='Relation.additional_information', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_RELATION_ADDITIONALINFORMATIONENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1028,
  serialized_end=1204,
)


_ANNOTATIONSET = _descriptor.Descriptor(
  name='AnnotationSet',
  full_name='AnnotationSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tracks_groups', full_name='AnnotationSet.tracks_groups', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temporal_relations', full_name='AnnotationSet.temporal_relations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='surgery_id', full_name='AnnotationSet.surgery_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1206,
  serialized_end=1317,
)


_ANNOTATIONMODELDEFINITION = _descriptor.Descriptor(
  name='AnnotationModelDefinition',
  full_name='AnnotationModelDefinition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity_types', full_name='AnnotationModelDefinition.entity_types', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='AnnotationModelDefinition.constraints', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='AnnotationModelDefinition.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='instructions_id', full_name='AnnotationModelDefinition.instructions_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1320,
  serialized_end=1460,
)

_TEMPORALINTERVAL.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TEMPORALINTERVAL.fields_by_name['end'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TEMPORALPOINT.fields_by_name['point'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SPATIALSPAN.fields_by_name['elements'].message_type = _COORDINATE2D
_EVENT.fields_by_name['temporal_interval'].message_type = _TEMPORALINTERVAL
_EVENT.fields_by_name['temporal_point'].message_type = _TEMPORALPOINT
_EVENT.fields_by_name['spatial_span'].message_type = _SPATIALSPAN
_EVENT.oneofs_by_name['temporal_span'].fields.append(
  _EVENT.fields_by_name['temporal_interval'])
_EVENT.fields_by_name['temporal_interval'].containing_oneof = _EVENT.oneofs_by_name['temporal_span']
_EVENT.oneofs_by_name['temporal_span'].fields.append(
  _EVENT.fields_by_name['temporal_point'])
_EVENT.fields_by_name['temporal_point'].containing_oneof = _EVENT.oneofs_by_name['temporal_span']
_EVENT.oneofs_by_name['temporal_span'].fields.append(
  _EVENT.fields_by_name['temporal_constant'])
_EVENT.fields_by_name['temporal_constant'].containing_oneof = _EVENT.oneofs_by_name['temporal_span']
_SURGERYENTITY.fields_by_name['event'].message_type = _EVENT
_SURGERYENTITY.fields_by_name['object'].message_type = _SURGICALOBJECT
_SURGERYENTITY.fields_by_name['external_entity'].message_type = _EXTERNALENTITY
_SURGERYENTITY.oneofs_by_name['type'].fields.append(
  _SURGERYENTITY.fields_by_name['event'])
_SURGERYENTITY.fields_by_name['event'].containing_oneof = _SURGERYENTITY.oneofs_by_name['type']
_SURGERYENTITY.oneofs_by_name['type'].fields.append(
  _SURGERYENTITY.fields_by_name['object'])
_SURGERYENTITY.fields_by_name['object'].containing_oneof = _SURGERYENTITY.oneofs_by_name['type']
_SURGERYENTITY.oneofs_by_name['type'].fields.append(
  _SURGERYENTITY.fields_by_name['external_entity'])
_SURGERYENTITY.fields_by_name['external_entity'].containing_oneof = _SURGERYENTITY.oneofs_by_name['type']
_TRACK.fields_by_name['entities'].message_type = _SURGERYENTITY
_TRACKSGROUP.fields_by_name['tracks'].message_type = _TRACK
_RELATION_ADDITIONALINFORMATIONENTRY.containing_type = _RELATION
_RELATION.fields_by_name['additional_information'].message_type = _RELATION_ADDITIONALINFORMATIONENTRY
_ANNOTATIONSET.fields_by_name['tracks_groups'].message_type = _TRACKSGROUP
_ANNOTATIONSET.fields_by_name['temporal_relations'].message_type = _RELATION
_ANNOTATIONMODELDEFINITION.fields_by_name['entity_types'].message_type = _SURGICALOBJECT
_ANNOTATIONMODELDEFINITION.fields_by_name['constraints'].message_type = _RELATION
DESCRIPTOR.message_types_by_name['SurgicalObject'] = _SURGICALOBJECT
DESCRIPTOR.message_types_by_name['ExternalEntity'] = _EXTERNALENTITY
DESCRIPTOR.message_types_by_name['TemporalInterval'] = _TEMPORALINTERVAL
DESCRIPTOR.message_types_by_name['TemporalPoint'] = _TEMPORALPOINT
DESCRIPTOR.message_types_by_name['Coordinate2D'] = _COORDINATE2D
DESCRIPTOR.message_types_by_name['SpatialSpan'] = _SPATIALSPAN
DESCRIPTOR.message_types_by_name['Event'] = _EVENT
DESCRIPTOR.message_types_by_name['SurgeryEntity'] = _SURGERYENTITY
DESCRIPTOR.message_types_by_name['Track'] = _TRACK
DESCRIPTOR.message_types_by_name['TracksGroup'] = _TRACKSGROUP
DESCRIPTOR.message_types_by_name['Relation'] = _RELATION
DESCRIPTOR.message_types_by_name['AnnotationSet'] = _ANNOTATIONSET
DESCRIPTOR.message_types_by_name['AnnotationModelDefinition'] = _ANNOTATIONMODELDEFINITION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SurgicalObject = _reflection.GeneratedProtocolMessageType('SurgicalObject', (_message.Message,), {
  'DESCRIPTOR' : _SURGICALOBJECT,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:SurgicalObject)
  })
_sym_db.RegisterMessage(SurgicalObject)

ExternalEntity = _reflection.GeneratedProtocolMessageType('ExternalEntity', (_message.Message,), {
  'DESCRIPTOR' : _EXTERNALENTITY,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:ExternalEntity)
  })
_sym_db.RegisterMessage(ExternalEntity)

TemporalInterval = _reflection.GeneratedProtocolMessageType('TemporalInterval', (_message.Message,), {
  'DESCRIPTOR' : _TEMPORALINTERVAL,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:TemporalInterval)
  })
_sym_db.RegisterMessage(TemporalInterval)

TemporalPoint = _reflection.GeneratedProtocolMessageType('TemporalPoint', (_message.Message,), {
  'DESCRIPTOR' : _TEMPORALPOINT,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:TemporalPoint)
  })
_sym_db.RegisterMessage(TemporalPoint)

Coordinate2D = _reflection.GeneratedProtocolMessageType('Coordinate2D', (_message.Message,), {
  'DESCRIPTOR' : _COORDINATE2D,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:Coordinate2D)
  })
_sym_db.RegisterMessage(Coordinate2D)

SpatialSpan = _reflection.GeneratedProtocolMessageType('SpatialSpan', (_message.Message,), {
  'DESCRIPTOR' : _SPATIALSPAN,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:SpatialSpan)
  })
_sym_db.RegisterMessage(SpatialSpan)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), {
  'DESCRIPTOR' : _EVENT,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:Event)
  })
_sym_db.RegisterMessage(Event)

SurgeryEntity = _reflection.GeneratedProtocolMessageType('SurgeryEntity', (_message.Message,), {
  'DESCRIPTOR' : _SURGERYENTITY,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:SurgeryEntity)
  })
_sym_db.RegisterMessage(SurgeryEntity)

Track = _reflection.GeneratedProtocolMessageType('Track', (_message.Message,), {
  'DESCRIPTOR' : _TRACK,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:Track)
  })
_sym_db.RegisterMessage(Track)

TracksGroup = _reflection.GeneratedProtocolMessageType('TracksGroup', (_message.Message,), {
  'DESCRIPTOR' : _TRACKSGROUP,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:TracksGroup)
  })
_sym_db.RegisterMessage(TracksGroup)

Relation = _reflection.GeneratedProtocolMessageType('Relation', (_message.Message,), {

  'AdditionalInformationEntry' : _reflection.GeneratedProtocolMessageType('AdditionalInformationEntry', (_message.Message,), {
    'DESCRIPTOR' : _RELATION_ADDITIONALINFORMATIONENTRY,
    '__module__' : 'data_interface.sages_pb2'
    # @@protoc_insertion_point(class_scope:Relation.AdditionalInformationEntry)
    })
  ,
  'DESCRIPTOR' : _RELATION,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:Relation)
  })
_sym_db.RegisterMessage(Relation)
_sym_db.RegisterMessage(Relation.AdditionalInformationEntry)

AnnotationSet = _reflection.GeneratedProtocolMessageType('AnnotationSet', (_message.Message,), {
  'DESCRIPTOR' : _ANNOTATIONSET,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:AnnotationSet)
  })
_sym_db.RegisterMessage(AnnotationSet)

AnnotationModelDefinition = _reflection.GeneratedProtocolMessageType('AnnotationModelDefinition', (_message.Message,), {
  'DESCRIPTOR' : _ANNOTATIONMODELDEFINITION,
  '__module__' : 'data_interface.sages_pb2'
  # @@protoc_insertion_point(class_scope:AnnotationModelDefinition)
  })
_sym_db.RegisterMessage(AnnotationModelDefinition)


_RELATION_ADDITIONALINFORMATIONENTRY._options = None
# @@protoc_insertion_point(module_scope)
