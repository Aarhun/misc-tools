#!/usr/bin/python
"""
Tool to parse, sort and write OPML youtube subscription file.
"""
import logging
import sys
import argparse
import xml.dom.minidom
import cgi

LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler(sys.stdout)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

class Rss(object): #pylint: disable=too-few-public-methods 
    """
    Class to handle rss subscription.
    """
    def __init__(self, rss):
        self.text = rss.getAttribute("text")
        self.title = rss.getAttribute("title")
        self.type = rss.getAttribute("type")
        self.xml_url = rss.getAttribute("xmlUrl")
        LOGGER.debug("TEXT %s", self.text)
        LOGGER.debug("TITLE %s", self.title)
        LOGGER.debug("TYPE %s", self.type)
        LOGGER.debug("XMLURL %s", self.xml_url)

class Category(object): #pylint: disable=too-few-public-methods 
    """
    Class to handle category.
    """
    def __init__(self, category):
        self.text = category.getAttribute("text")
        self.title = category.getAttribute("title")
        LOGGER.debug("TEXT %s", self.text)
        LOGGER.debug("TITLE %s", self.title)


def write_opml(output_file, rss_dict):
    """
    Write OPML file.
    """
    output_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    output_file.write('<opml version="1.1">\n')
    output_file.write('\t<body>\n')
    for category in rss_dict.keys():
        output_file.write(('\t\t<outline text="%s" title="%s">\n' % \
            (cgi.escape(category.text), cgi.escape(category.title))).encode('utf-8'))
        for rss in rss_dict[category]:
            output_file.write(('\t\t\t<outline text="%s" title="%s" type="rss" xmlUrl="%s"/>\n' % \
                (cgi.escape(rss.text), cgi.escape(rss.title), rss.xml_url)).encode('utf-8'))

        output_file.write('\t\t</outline>\n')
    output_file.write('\t</body>\n')
    output_file.write('</opml>\n')

def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description='A tool to parse and sort \
                                     OPML youtube subsription file', \
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_file', help='File path to read.')
    parser.add_argument('output_file', help='File path to write.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode.')

    args = parser.parse_args()

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    rss_dict = {}
    my_dom = xml.dom.minidom.parse(args.input_file)
    for body in my_dom.documentElement.childNodes:
        if body.localName in ['body']:
            for outline in body.childNodes:
                if outline.localName in ['outline']:
                    cat = Category(outline)
                    rss_list = []
                    for rss in outline.childNodes:
                        LOGGER.debug(rss)
                        if rss.nodeType == rss.ELEMENT_NODE and \
                           rss.getAttribute('type') == 'rss' and \
                           rss.hasAttribute('xmlUrl'):
                            rss_list.append(Rss(rss))
                    rss_list = sorted(rss_list, key=lambda rss: rss.title.lower())
                    rss_dict[cat] = rss_list


    output_file = open(args.output_file, 'w')
    write_opml(output_file, rss_dict)
    output_file.close()



if __name__ == "__main__":
    main()
