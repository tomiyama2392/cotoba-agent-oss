"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest
import os

from programy.processors.post.removehtml import RemoveHTMLPostProcessor
from programy.context import ClientContext

from programytest.client import TestClient


class RemoveHTMLTests(unittest.TestCase):

    def test_remove_html(self):
        processor = RemoveHTMLPostProcessor()

        context = ClientContext(TestClient(), "testid")

        result = processor.process(context, "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = processor.process(context, "Hello <br/> World")
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual("Hello\nWorld", result)
        elif os.name == 'nt':
            self.assertEqual("Hello\r\nWorld", result)
        else:
            raise Exception("Unknown os [%s]" % os.name)

        result = processor.process(context, "Hello <br /> World")
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual("Hello\nWorld", result)
        elif os.name == 'nt':
            self.assertEqual("Hello\r\nWorld", result)
        else:
            raise Exception("Unknown os [%s]" % os.name)
