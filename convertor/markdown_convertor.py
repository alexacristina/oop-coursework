#!/usr/bin/python2

import re
from sys import argv
import urllib2


class MarkdownParser(object):
    text = ""
    header_regex = re.compile(r'(?:^|\n)(#{1,6}(?!#).+?)(?:$|\n)')
    bold_regex = re.compile(
            r'(?:^|\n|\s|\[)(\*\*.+?\*\*)(?!`)(?:\n|\s|$|\])'
        )

    italic_regex = re.compile(r'[^*`](\*[^*].+?\*)')

    bold_code_regex = re.compile(r'(`\*.+?\*`)')
    code_regex = re.compile(r'(`(?!\*).+?(?!\*)`)')
    link_regex = re.compile(r'(\[.+?\]\(.+?\))')
    paragraph = re.compile(r'((?:[^\n]+\n(?!%s))+)\n*' % (
            header_regex
        )
    )

    def __init__(self, text_to_parse=''):
        self.text = text_to_parse

    def __get_params__(self, regex_type):
        text_list = list()
        regex_texts = regex_type.findall(self.text)
        for regex_text in regex_texts:
            match = re.search(re.escape(regex_text), self.text)
            start_match = match.start()
            end_match = match.end()
            text_list.append([
                regex_text,
                start_match,
                end_match
            ])
        return text_list

    def file_to_text(self, filename):
        with open(filename, 'r') as file_to_parse:
            self.text = file_to_parse.read()

    def find_header(self):
        headers_list = []
        headers = self.header_regex.findall(self.text)
        for header in headers:
            match = re.search(header, self.text)
            nr_hashes = header.count('#', 0, 6)
            start_match = match.start()
            end_match = match.end()
            headers_list.append([
                header,
                start_match,
                end_match,
                nr_hashes
            ])
        return headers_list

    def find_bold(self):
        bold_list = self.__get_params__(self.bold_regex)
        return bold_list

    def find_italic(self):
        italic_list = self.__get_params__(self.italic_regex)
        return italic_list

    def find_code(self):
        code_list = self.__get_params__(self.code_regex)
        return code_list

    def find_bcode(self):
        bcode_list = self.__get_params__(self.bold_code_regex)
        return bcode_list

    def find_link(self):
        link_list = self.__get_params__(self.link_regex)
        return link_list

    def find_paragraph(self):
        paragraph_list = list()
        paragraph_texts = self.paragraph.findall(self.text)
        for paragraph_text in paragraph_texts:
            if self.header_regex.findall(paragraph_text):
                paragraph_text = self.header_regex.sub('', paragraph_text)
            match = re.search(re.escape(paragraph_text), self.text)
            start_match = match.start()
            end_match = match.end()
            paragraph_list.append([
                paragraph_text,
                start_match,
                end_match
            ])
        return paragraph_list


class HTMLRenderer(object):

    text_to_render = ""
    rendered_text = ""

    def __init__(self, text_to_render):
        self.text_to_render = text_to_render
        self.markdown_parser = MarkdownParser(self.text_to_render)

    def __replace_all__(self, dic):
        for i, j in dic.iteritems():
            self.text_to_render = self.text_to_render.replace(i, j)
        return self.text_to_render

    def render_header(self):
        html_headers = list()
        header_list = self.markdown_parser.find_header()
        for header in header_list:
            regex = re.compile(r'(?:#{1,6}\s)(.+)')
            new_header = re.findall(regex, header[0])
            new_string = "\n<h" + str(header[3]) + ">" + \
                new_header[0] + "</h" + str(header[3]) + ">\n"
            html_headers.append([new_string, header[1], header[2]])
        return html_headers

    def render_bold(self):
        html_bold = list()
        bold_list = self.markdown_parser.find_bold()
        for item in bold_list:
            new_item = re.findall(r'\*\*(.+)\*\*$', item[0])
            new_string = '<strong>' + new_item[0] + '</strong>'
            html_bold.append([new_string, item[1], item[2], item[0]])
        return html_bold

    def render_italic(self):
        html_italic = list()
        italic_list = self.markdown_parser.find_italic()
        for item in italic_list:
            new_item = re.findall(r'(?:\*(.+)\*)$', item[0])
            new_string = '<em>' + new_item[0] + '</em>'
            html_italic.append([new_string, item[1], item[2], item[0]])
        return html_italic

    def render_code(self):
        html_code = list()
        code_list = self.markdown_parser.find_code()
        for item in code_list:
            new_item = re.findall(r'`(.+)`', item[0])
            new_string = '<code>' + new_item[0] + '</code>'
            html_code.append([new_string, item[1], item[2], item[0]])
        return html_code

    def render_bcode(self):
        html_bcode = list()
        bcode_list = self.markdown_parser.find_bcode()
        for item in bcode_list:
            new_item = re.findall(r'`\*(.+)\*`', item[0])
            new_string = '<code><strong>' + new_item[0] + '</strong></code>'
            html_bcode.append([new_string, item[1], item[2], item[0]])
        return html_bcode

    def render_link(self):
        html_link = list()
        link_list = self.markdown_parser.find_link()
        for item in link_list:
            new_item = re.findall(r'\[(.+)\]\((.+)\)', item[0])
            new_string = ''.join([
                    '<a href="', new_item[0][1],
                     '" rel="noreferrer" class="hoverZoomLink">',
                    new_item[0][0],
                    '</a>'
                ])
            html_link.append([new_string, item[1], item[2], item[0]])
        return html_link

    def render_paragraph(self):
        html_paragraph = list()
        paragraph_list = self.markdown_parser.find_paragraph()
        for item in paragraph_list:
            new_item = item[0][:-1]
            new_string = '\n<p>' + new_item + '</p>\n'
            html_paragraph.append([new_string, item[1], item[2]])
        return html_paragraph


class Convertor(object):

    def __init__(self, input, output_filename):
        self.html_list = list()
        self.input = input
        self.output_filename = output_filename

    def initialize_list(self):
        self.html_list.extend(
            self.htmlrenderer.render_header() +
            self.htmlrenderer.render_bold() +
            self.htmlrenderer.render_italic() +
            self.htmlrenderer.render_code() +
            self.htmlrenderer.render_bcode() +
            self.htmlrenderer.render_link() +
            self.htmlrenderer.render_paragraph()
        )

    def sort_list(self):
        return sorted(self.html_list, key=lambda x: x[1])

    def separate_block_inlines(self):
        inline_items = list()
        block_items = list()
        sorted_html = self.sort_list()
        for item in sorted_html:
            if item[0][-1] == '\n':
                block_items.append(item)
            else:
                inline_items.append(item)
        return block_items, inline_items

    def insert_items_into_blocks(self, inline_items):
        self.html_list = self.sort_list()
        for item in self.html_list:
            for inline_item in inline_items:
                if (inline_item[3] in item[0]) & (inline_item[3] != item[0]):
                    splitted = item[0].split(inline_item[3])
                    new_block = ''.join([splitted[0],
                                         inline_item[0],
                                         splitted[1]])
                    item[0] = new_block

    def block_write_to_file(self, block_items):
        with open(self.output_filename, 'w+') as output:
            for item in block_items:
                output.write(item[0])
            output.close()

    def inline_write_to_file(self, inline_items):
        sorted_inline = sorted(inline_items,
                               key=lambda x: x[2] - x[1],
                               reverse=True)
        with open(self.output_filename, 'r+') as output1:
            for line in output1.readlines():
                for item in sorted_inline:
                    if item[3] in line:
                        new_line = line.replace(item[3], item[0])
                        output1.write(new_line)
            output1.close()

    def write_to_file(self):
        block_items, inline_items = self.separate_block_inlines()
        block_items[0][0] = re.findall(
                re.compile('^(?!\s)|^\s(.+\s)'),
                block_items[0][0]
            )[0]
        block_items[-1][0] = re.findall(
            re.compile('(\n.+)\n$'),
            block_items[-1][0]
        )[0]
        self.block_write_to_file(block_items)

    def convert_to_html(self):
        self.initialize_list()
        spam, items = self.separate_block_inlines()
        self.insert_items_into_blocks(items)


class ConvertorFile(Convertor):
    def __init__(self, input, output_filename):
        with open(input, 'r') as markdown_file:
            text_to_render = markdown_file.read()
        self.htmlrenderer = HTMLRenderer(text_to_render)
        super(ConvertorFile, self).__init__(input, output_filename)


class ConvertorURL(Convertor):

    def __init__(self, input, output_filename):
        data = urllib2.urlopen(input)
        self.htmlrenderer = HTMLRenderer(data.read())
        super(ConvertorURL, self).__init__(input, output_filename)


def run(argv):
    convertor = ConvertorURL(argv[1], argv[2])
    convertor.convert_to_html()
    convertor.write_to_file()
    myconvertor = ConvertorFile('input.md', 'myoutput.md')
    myconvertor.convert_to_html()
    myconvertor.write_to_file()


if __name__ == "__main__":
    run(argv)
