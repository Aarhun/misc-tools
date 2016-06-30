#!/usr/bin/python
"""
Tool to parse, sort and write OPML youtube subscription file.
"""
import logging
import sys
import argparse
import xml.dom.minidom

LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler(sys.stdout)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

class Rss(object): # pylint: disable=too-few-public-methods 
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

def write_opml(output_file, rss_list):
    """
    Write OPML file.
    """
    output_file.write('<opml version="1.1">\n')
    output_file.write('<body>\n')
    output_file.write('<outline text="YouTube Subscriptions" title="YouTube Subscriptions">\n')
    for rss in rss_list:
        output_file.write(('<outline text="%s" title="%s" type="rss" xmlUrl="%s"/>\n' % (rss.text, rss.title, rss.xml_url)).encode('utf-8'))

    output_file.write('</outline>\n')
    output_file.write('</body>\n')
    output_file.write('</opml>\n')

def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description='A tool to parse and sort OPML youtube subsription file', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_file', help='File path to read.')
    parser.add_argument('output_file', help='File path to write.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode.')

    args = parser.parse_args()

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
    
    rss_list = []
    my_dom = xml.dom.minidom.parse(args.input_file)
    for body in my_dom.documentElement.childNodes:
        if body.localName in ['body']:
            for outline in body.childNodes:
                if outline.localName in ['outline']:
                    for rss in outline.childNodes:
                        if rss.getAttribute('type') == 'rss' and rss.hasAttribute('xmlUrl'):
                            rss_list.append(Rss(rss))


    rss_list = sorted(rss_list, key=lambda rss: rss.title.lower())
    output_file = open(args.output_file, 'w')
    write_opml(output_file, rss_list)
    output_file.close()



if __name__ == "__main__":
    main()
