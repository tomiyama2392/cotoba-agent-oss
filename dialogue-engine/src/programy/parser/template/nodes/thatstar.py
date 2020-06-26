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
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.indexed import TemplateTripleIndexedNode
from programy.parser.exceptions import ParserException


class TemplateThatStarNode(TemplateTripleIndexedNode):

    def __init__(self, star=1, question=1, sentence=1):
        TemplateTripleIndexedNode.__init__(self, star, question, sentence)

    def resolve_to_string(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)

        try:
            question = conversation.previous_nth_question(self.question - 1)
            sentence = question.current_sentence()
            resolved = sentence.matched_context.thatstar(self.star)
            if resolved is None:
                YLogger.debug(client_context, "ThatStar failed")
                resolved = ""
        except Exception:
            YLogger.debug(client_context, "ThatStar failed")
            resolved = ""

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        string = "[THATSTAR"
        string += self.get_star_and_question_and_sentence_as_str() + "]"
        return string

    def to_xml(self, client_context):
        xml = "<thatstar"
        xml += self.get_star_and_question_and_sentence_as_index_xml()
        xml += "></thatstar>"
        return xml

    #######################################################################################################
    # THATSTAR_EXPRESSION ::== <thatstar( INDEX_ATTRIBUTE)/> | <thatstar><index>TEMPLATE_EXPRESSION</index></thatstar>

    def parse_expression(self, graph, expression):
        try:
            self._parse_node_with_attrib(graph, expression, "index", "1,1,1")
        except ParserException as excep:
            excep.nodename = 'thatstar'
            raise

        if self.children:
            raise ParserException("Node should not contain child text", xml_element=expression, nodename='topicstar')
