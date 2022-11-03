# Copyright (c) 2022, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy

from cugraph_service_client.cugraph_service_thrift import spec

Value = spec.Value
GraphVertexEdgeID = spec.GraphVertexEdgeID
BatchedEgoGraphsResult = spec.BatchedEgoGraphsResult
Node2vecResult = spec.Node2vecResult
UniformNeighborSampleResult = spec.UniformNeighborSampleResult


class UnionWrapper:
    """
    Provides easy conversions between py objs and Thrift "unions". This is used
    as a base class for the "*Wrapper" classes below. Together with the derived
    classes below, these objects allow the caller to go from py objects/Thrift
    unions to Thrift unions/py objects.
    """

    def get_py_obj(self):
        """
        Get the python object set in the union.
        """
        not_members = set(["default_spec", "thrift_spec", "read", "write"])
        attrs = [
            a
            for a in dir(self.union)
            if not (a.startswith("_")) and a not in not_members
        ]
        # Much like a C union, only one field will be set. Return the first
        # non-None value encountered.
        for a in attrs:
            val = getattr(self.union, a)
            if val is not None:
                return val

        return None


class ValueWrapper(UnionWrapper):
    """
    Provides an easy-to-use python object for abstracting Thrift "unions",
    allowing a python obj to be automatically mapped to the correct union
    field.
    """

    def __init__(self, val, val_name="value"):
        """
        Construct with a value supported by the Value "union". See
        cugraph_service_thrift.py

        val_name is used for better error messages only, and can be passed for
        including in the exception thrown if an invalid type is passed here.
        """
        if isinstance(val, Value):
            self.union = val
        elif isinstance(val, int):
            if val < 4294967296:
                self.union = Value(int32_value=val)
            else:
                self.union = Value(int64_value=val)
        elif isinstance(val, numpy.int32):
            self.union = Value(int32_value=int(val))
        elif isinstance(val, numpy.int64):
            self.union = Value(int64_value=int(val))
        elif isinstance(val, str):
            self.union = Value(string_value=val)
        elif isinstance(val, bool):
            self.union = Value(bool_value=val)
        else:
            raise TypeError(
                f"{val_name} must be one of the "
                "following types: [int, str, bool], got "
                f"{type(val)}"
            )


class GraphVertexEdgeIDWrapper(UnionWrapper):
    def __init__(self, val, val_name="id"):
        if isinstance(val, GraphVertexEdgeID):
            self.union = val
        elif isinstance(val, int):
            if val >= 4294967296:
                self.union = GraphVertexEdgeID(int64_id=val)
            else:
                self.union = GraphVertexEdgeID(int32_id=val)
        elif isinstance(val, list):
            # FIXME: this only check the first item, others could be larger
            if val[0] >= 4294967296:
                self.union = GraphVertexEdgeID(int64_ids=val)
            else:
                self.union = GraphVertexEdgeID(int32_ids=val)
        else:
            raise TypeError(
                f"{val_name} must be one of the "
                "following types: [int, list<int>], got "
                f"{type(val)}"
            )