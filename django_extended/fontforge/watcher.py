
import os
import sys
import time
import logging
import signal
import tempfile

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

from django import conf
from django.conf import settings
from django.utils.module_loading import import_module
from django.db.models import get_models, get_app

import subprocess

try:
    FONTFORGE_EXISTS = True
    from libs import original_fontforge as fontforge
except:
    FONTFORGE_EXISTS = False

DEFAULT_FONT_FORMATS = ('ttf', 'otf', 'eot', 'svg', 'woff')


class EventHandler(FileSystemEventHandler):

    def __init__(self, watcher, *args, **kwargs):
        self.watcher = watcher
        super(EventHandler, self).__init__( *args, **kwargs)

    def on_any_event(self, event):
        self.watcher.process_changes(event)

class Watcher(object):
    handler = None
    command = None
    blocked = False
    stout_prefix = 'fontforge'
    configs = []

    def __init__(self, command=None, *args, **kwargs):
        #self.handler = WatcherHandler(self)
        self.command = command
        self.observer = Observer()
        self.event_handler = EventHandler(self)


        # self.notifier.max_user_watches=16384
        self.process_settings()

        paths = self.get_watched_paths()
        for appname, path in paths:
            try:
                self.observer.schedule(self.event_handler, path, recursive=True)
                self.print_head('Watching \033[94m%s\033[0m' % (appname))
            except Exception, e:
                self.print_error('Watching %s error : %s' % (appname, str(e)))

    def process_changes(self, event):

        if event.src_path.endswith('.sfd'):
            if FONTFORGE_EXISTS:
                from subprocess import call
                call(["python", "manage.py", "fontforge_generate"])
                # self.generate_font()
            else:

                self.print_error("Python bindings for fontforge are not installed (try sudo apt-get install python-fontforge)")


    def process_settings(self):

        reload(conf)
        reload(fontforge)
        self.configs = []
        settings = conf.settings

        if not hasattr(settings, 'FONTFORGE_WATCHER') and 'watcher' in settings.FONTFORGE_WATCHER:
            self.print_error('settings.FONTFORGE_WATCHER is missing ')
        else:
            configs = settings.FONTFORGE_WATCHER

            for config in configs:

                try:

                    source = config[0]
                    folder_output = config[1]
                    css_output = config[2] if len(config) >= 3 else None
                    classname = config[3] if len(config) >= 4 else None
                    content = None

                    if not os.path.isfile(source):
                        source = os.path.join(dirname(settings.DJANGO_ROOT), config[0])
                        if not os.path.isfile(source):
                            self.print_error('Source is missing "%s"' % source)
                            source = None

                    if source:
                        f = open(source, 'r')
                        content = f.read()
                        f.close()

                    if not os.path.isdir(folder_output):
                        folder_output = os.path.join(dirname(settings.DJANGO_ROOT), folder_output)
                        if not os.path.isdir(folder_output):
                            self.print_error('Folder output is missing "%s"' % folder_output)
                            folder_output = None

                    css_output_dir = os.path.dirname(css_output)
                    if not os.path.isdir(css_output_dir):
                        css_output_dir = os.path.join(dirname(settings.DJANGO_ROOT), css_output_dir)
                        css_output =    os.path.join(dirname(settings.DJANGO_ROOT), css_output)
                        if not os.path.isdir(css_output_dir):
                            self.print_error('CSS output folder is missing "%s"' % css_output)
                            css_output = None

                    if source and folder_output:
                        self.configs.append([source, folder_output, css_output, classname, content])
                except Exception, e:
                    self.print_error('Invalid config for fontforge watcher "%s"' % str(e))


    def generate(self,  compress=True):
        self.generate_font(compress=compress)


    def generate_font(self,  compress=True):

        self.process_settings()
        for config in self.configs:

            f = open(config[0], 'r')
            content = f.read()
            f.close()
            if True:#content != config[4]:
                self.print_head('Changes detected (%s)' % config[0])
                config[4] = content
                try:
                    source = config[0]
                    name = os.path.basename(source).split('.')[0]
                    folder_output = os.path.join(config[1], name)
                    css_output = config[2]
                    classname = config[3]
                    font = fontforge.open(source)
                    if css_output and classname:
                        css = """
@font-face {
    font-family: '%(font_name)s';
    src: url('../fonts/%(font_name)s/%(font_name)s.eot');
    src: url('../fonts/%(font_name)s/%(font_name)s.eot?#iefix') format('eot'),
         url('../fonts/%(font_name)s/%(font_name)s.woff') format('woff'),
         url('../fonts/%(font_name)s/%(font_name)s.svg#%(font_name)s') format('svg'),
         url('../fonts/%(font_name)s/%(font_name)s.ttf') format('truetype');
    font-style: normal;
    font-weight: normal;
}

.%(font_classname)s {
    position: relative;
    display: inline-block;
    top: 1px;
    font-family: '%(font_name)s';
    font-style: normal;
    font-weight: normal;
    line-height: 1;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

""" % {
                    'font_name' : name,
                    'font_classname' : classname
                }
                        for glyph in font.glyphs():
                            if not glyph.glyphname.startswith('uni'):
                                print glyph.glyphname
                            css += """.%(font_classname)s-%(glyph_name)s:before { content: "\\%(glyph_unicode)s"; }\n""" % {
                                'font_classname' : classname,
                                'glyph_name' : glyph.glyphname,
                                'glyph_unicode' : "%04X" % (glyph.unicode)
                            }

                    for format in DEFAULT_FONT_FORMATS:
                        folder = os.path.join(folder_output, name)
                        filename = "%s.%s" % (folder, format)
                        self.print_process('Compiling %s' % filename)

                        if not os.path.exists(folder):
                            os.makedirs(folder)

                        font.generate(filename)
                        self.print_success('Done')

                    self.print_process('Pushing font css glyphs into %s' % css_output)
                    try:
                        os.remove(css_output)
                    except:
                        pass
                    css_file = open("%s" % css_output, "w+")
                    css_file.write(css)
                    css_file.close()
                    self.print_success("Done (%s chars)." % len(css))
                except Exception, e:
                    self.print_error('Error during font generation : %s' % (str(e)))
            else:
                self.print_head("No changes")




    def get_watched_paths(self):
        app_paths = []
        for config in self.configs:
            source_dir = os.path.abspath(os.path.dirname(config[0]))
            app_paths.append(
                (config[0], source_dir)
            )
        return app_paths

    def sigterm(self, signum, frame):
        self.observer.stop()
        self.observer.join()
        exit(0)

    def watch(self, paths=[]):

        signal.signal(signal.SIGTERM, self.sigterm)
        signal.signal(signal.SIGINT , self.sigterm)
        logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


    def print_r(self, pattern, str):
        output = pattern % (self.stout_prefix, str)
        if self.command:
            self.command.stdout.write(output)
            self.command.stdout.flush()
        else:
            print output

    def print_head(self, str):
        self.print_r("\033[95m[%s]\033[0m %s", str)

    def print_process(self, str):
        self.print_r("\033[95m[%s]\033[0m \033[93m%s\033[0m", str)

    def print_success(self, str):
        self.print_r("\033[95m[%s]\033[0m \033[92m%s\033[0m", str)

    def print_error(self, str):
        self.print_r("\033[95m[%s]\033[0m \033[91m%s\033[0m", str)
