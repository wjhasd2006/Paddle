#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

from __future__ import print_function

import gast
import six
import unittest

from paddle.fluid.dygraph.dygraph_to_static.utils import ast_to_source_code
from paddle.fluid.dygraph.dygraph_to_static.variable_trans_func import create_fill_constant_node


class TestVariableTransFunc(unittest.TestCase):
    def test_create_fill_constant_node(self):
        node = create_fill_constant_node("a", 1.0)
        source = "a = fluid.layers.fill_constant(shape=[1], dtype='float64', value=1.0)"
        self.assertEqual(ast_to_source_code(node).strip(), source)

        node = create_fill_constant_node("b", True)
        source = "b = fluid.layers.fill_constant(shape=[1], dtype='bool', value=True)"
        self.assertEqual(ast_to_source_code(node).strip(), source)

        if six.PY2:
            node = create_fill_constant_node("c", 214)
            source = "c = fluid.layers.fill_constant(shape=[1], dtype='int32', value=214)"
            self.assertEqual(ast_to_source_code(node).strip(), source)

            node = create_fill_constant_node("d", long(10086))
            source = "d = fluid.layers.fill_constant(shape=[1], dtype='int64', value=10086)"
            self.assertEqual(ast_to_source_code(node).strip(), source)
        else:
            node = create_fill_constant_node("c", 4293)
            source = "c = fluid.layers.fill_constant(shape=[1], dtype='int64', value=4293)"
            self.assertEqual(ast_to_source_code(node).strip(), source)

        self.assertIsNone(create_fill_constant_node("e", None))
        self.assertIsNone(create_fill_constant_node("e", []))


if __name__ == '__main__':
    unittest.main()