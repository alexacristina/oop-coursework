# -*- coding: utf-8 -*-

from lettuce import *
from os.path import *
import sys
import filecmp
import urllib2

ROOT_PATH = dirname(dirname(dirname(abspath(__file__))))

sys.path.append(ROOT_PATH)

from convertor import markdown_convertor


@step(u'Given I load the markdown file \'([^\']*)\' with the output \'([^\']*)\'')
def given_i_load_the_markdown_file_group1_with_the_output_group2(step,
                                                                 group1,
                                                                 group2):
    world.input = ''.join(['%s/', str(group1)]) % ROOT_PATH
    world.output = ''.join(['%s/', str(group2)]) % ROOT_PATH
    world.convertor = markdown_convertor.ConvertorFile(
        world.input,
        world.output
    )
    assert world.input.lower().endswith('.md')


@step(u'When I convert it to HTML')
def convert_to_html(step):
    world.convertor.convert_to_html()
    assert world.output.lower().endswith('.html')


@step(u'Then I see the result of an HTML file similar to \'([^\']*)\'')
def then_i_see_the_result_of_an_html_file_similar_to_output(step, output):
    world.convertor.write_to_file()
    output_file = ''.join(['%s/', str(output)]) % ROOT_PATH
    assert (filecmp.cmp(
            world.convertor.output_filename,
            output_file,
            shallow=False))


@step(u'Given I load the markdown file from URL: \'([^\']*)\'')
def given_i_load_the_markdown_file_from_url_link(step, link):
    world.URLinput = link
    world.URLoutput = ''.join(['%s/', 'output_from_url.html']) % ROOT_PATH
    world.URLconvertor = markdown_convertor.ConvertorURL(
        world.URLinput,
        world.URLoutput
    )
    assert world.URLinput.lower().endswith('.md')


@step(u'When I convert the file to HTML')
def convert_it_to_html(step):
    world.URLconvertor.convert_to_html()
    assert world.URLoutput.lower().endswith('html')


@step(u'Then I see a result like the one at the URL: \'([^\']*)\'')
def then_i_see_a_result_like_the_one_at_the_URL_link(step, link):
    world.URLconvertor.write_to_file()
    world.data = urllib2.urlopen(link)
    count = 0
    with open(world.URLoutput, 'r') as output_file:
        for line1, line in zip(output_file, world.data):
            if line1 == line:
                count += 1
    assert count == 20
