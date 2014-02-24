# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Anima Istanbul
#
# This module is part of anima-tools and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import os
import edl


class PrevisBase(object):
    """The base for other Previs classes
    """

    def from_xml(self, xml_node):
        """Fills attributes with the given XML node

        :param xml_node: an xml.etree.ElementTree.Element instance
        """
        raise NotImplementedError

    def to_xml(self, indentation=2, pre_indent=0):
        """returns an xml version of this PrevisBase object
        """
        raise NotImplementedError


class NameMixin(object):
    """A mixin for name attribute
    """

    def __init__(self, name=''):
        self._name = self._validate_name(name)

    @classmethod
    def _validate_name(cls, name):
        """validates the given name value
        """
        if not isinstance(name, str):
            raise TypeError(
                '%(class)s.name should be a string, not %(name_class)s' % {
                    'class': cls.__name__,
                    'name_class': name.__class__.__name__
                }
            )
        return name

    @property
    def name(self):
        """returns the _name attribute
        """
        return self._name

    @name.setter
    def name(self, name):
        """setter for the name property
        """
        self._name = self._validate_name(name)


class DurationMixin(object):
    """A mixin for duration attribute
    """

    def __init__(self, duration=0.0):
        self._duration = self._validate_duration(duration)

    @classmethod
    def _validate_duration(cls, duration):
        """validates the given duration value
        """
        if duration is None:
            duration = 0.0

        if not isinstance(duration, (int, float)):
            raise TypeError(
                '%(class)s.duration should be an non-negative float, not '
                '%(duration_class)s' % {
                    'class': cls.__name__,
                    'duration_class': duration.__class__.__name__
                }
            )

        duration = float(duration)

        if duration < 0:
            raise ValueError(
                '%(class)s.duration should be an non-negative float' % {
                    'class': cls.__name__
                }
            )

        return duration

    @property
    def duration(self):
        """returns the _duration attribute value
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = self._validate_duration(duration)


class Sequence(PrevisBase):
    """XML compatibility class for Sequencer
    """

    def __init__(self):
        self.duration = None
        self.name = None
        self.rate = False
        self.timecode = '00:00:00:00'
        self.ntsc = False
        self.timebase = '24'
        self.media = None

    def from_xml(self, xml_node):
        """Fills attributes with the given XML node

        :param xml_node: an xml.etree.ElementTree.Element instance
        """
        self.duration = float(xml_node.find('duration').text)
        self.name = xml_node.find('name').text
        rate_tag = xml_node.find('rate')
        if rate_tag is not None:
            self.ntsc = rate_tag.find('ntsc').text.title() == 'True'
            self.timebase = rate_tag.find('timebase').text

        self.timecode = xml_node.find('timecode').find('string').text

        xml_media = xml_node.find('media')
        media = Media()
        media.from_xml(xml_media)

        self.media = media

    def to_xml(self, indentation=2, pre_indent=0):
        """returns an xml version of this Sequence object
        """
        template = """%(pre_indent)s<sequence>
%(pre_indent)s%(indentation)s<duration>%(duration)s</duration>
%(pre_indent)s%(indentation)s<name>%(name)s</name>
%(pre_indent)s%(indentation)s<rate>
%(pre_indent)s%(indentation)s%(indentation)s<ntsc>%(ntsc)s</ntsc>
%(pre_indent)s%(indentation)s%(indentation)s<timebase>%(timebase)s</timebase>
%(pre_indent)s%(indentation)s</rate>
%(pre_indent)s%(indentation)s<timecode>
%(pre_indent)s%(indentation)s%(indentation)s<string>%(timecode)s</string>
%(pre_indent)s%(indentation)s</timecode>
%(media)s
%(pre_indent)s</sequence>"""

        return template % {
            'duration': self.duration,
            'name': self.name,
            'ntsc': str(self.ntsc).upper(),
            'timebase': self.timebase,
            'timecode': self.timecode,
            'media': self.media.to_xml(indentation=indentation,
                                       pre_indent=indentation + pre_indent),
            'indentation': ' ' * indentation,
            'pre_indent': ' ' * pre_indent
        }


class Media(PrevisBase):
    """XML compatibility class for Sequencer
    """

    def __init__(self):
        self.video = []
        self.audio = []

    def from_xml(self, xml_node):
        """Fills attributes with the given XML node

        :param xml_node: an xml.etree.ElementTree.Element instance
        """
        xml_video_tags = xml_node.findall('video')
        for xml_video_tag in xml_video_tags:
            video = Video()
            video.from_xml(xml_video_tag)
            self.video.append(video)

    def to_xml(self, indentation=2, pre_indent=0):
        """returns an xml version of this Media object
        """
        template = """%(pre_indent)s<media>
%(videos)s
%(pre_indent)s</media>"""

        video_data = []
        for video in self.video:
            video_data.append(
                video.to_xml(indentation=indentation,
                             pre_indent=indentation + pre_indent)
            )
        video_data_as_str = '\n'.join(video_data)

        return template % {
            'videos': video_data_as_str,
            'pre_indent': ' ' * pre_indent,
            'indentation': ' ' * indentation
        }


class Video(PrevisBase):
    """XML compatibility class for Sequencer
    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.tracks = []

    def from_xml(self, xml_node):
        """Fills attributes with the given XML node

        :param xml_node: an xml.etree.ElementTree.Element instance
        """
        format = xml_node.find('format')
        self.width = int(
            format.find('samplecharacteristics').find('width').text
        )
        self.height = int(
            format.find('samplecharacteristics').find('height').text
        )

        # create tracks
        track_tag = xml_node.find('track')
        track = Track()
        track.from_xml(track_tag)

        self.tracks.append(track)

    def to_xml(self, indentation=2, pre_indent=0):
        """returns an xml version of this Video object
        """
        template = """%(pre_indent)s<video>
%(pre_indent)s%(indentation)s<format>
%(pre_indent)s%(indentation)s%(indentation)s<samplecharacteristics>
%(pre_indent)s%(indentation)s%(indentation)s%(indentation)s<width>%(width)s</width>
%(pre_indent)s%(indentation)s%(indentation)s%(indentation)s<height>%(height)s</height>
%(pre_indent)s%(indentation)s%(indentation)s</samplecharacteristics>
%(pre_indent)s%(indentation)s</format>
%(tracks)s
%(pre_indent)s</video>"""

        track_data = []
        for track in self.tracks:
            track_data.append(
                track.to_xml(indentation=indentation,
                             pre_indent=indentation + pre_indent)
            )
        track_data_as_str = '\n'.join(track_data)

        return template % {
            'width': self.width,
            'height': self.height,
            'tracks': track_data_as_str,
            'pre_indent': ' ' * pre_indent,
            'indentation': ' ' * indentation
        }


class Track(PrevisBase):
    """XML compatibility class for Sequencer
    """

    def __init__(self):
        self.locked = False
        self.enabled = True
        self.clips = []

    def from_xml(self, xml_node):
        """Fills attributes with the given XML node

        :param xml_node: an xml.etree.ElementTree.Element instance
        """
        self.locked = xml_node.find('locked').text.title() == 'True'
        self.enabled = xml_node.find('enabled').text.title() == 'True'

        # find clips
        for clip_tag in xml_node.findall('clipitem'):
            clip = Clip()
            clip.from_xml(clip_tag)
            self.clips.append(clip)

    def to_xml(self, indentation=2, pre_indent=0):
        """returns an xml version of this Track object
        """
        template = """%(pre_indent)s<track>
%(pre_indent)s%(indentation)s<locked>%(locked)s</locked>
%(pre_indent)s%(indentation)s<enabled>%(enabled)s</enabled>
%(clips)s
%(pre_indent)s</track>"""

        clip_data = []
        for clip in self.clips:
            clip_data.append(
                clip.to_xml(indentation=indentation,
                            pre_indent=indentation + pre_indent)
            )
        clip_data_as_str = '\n'.join(clip_data)

        return template % {
            'locked': str(self.locked).upper(),
            'enabled': str(self.enabled).upper(),
            'clips': clip_data_as_str,
            'pre_indent': ' ' * pre_indent,
            'indentation': ' ' * indentation
        }


class Clip(PrevisBase, NameMixin, DurationMixin):
    """XML compatibility class for Sequencer
    """

    def __init__(self, id=None, name='', start=0.0, end=0.0, duration=0.0,
                 enabled=True, in_=0, out=0):
        NameMixin.__init__(self, name=name)
        DurationMixin.__init__(self, duration=duration)
        self._id = self._validate_id(id)
        self.start = start
        self.end = end
        self.enabled = enabled
        self.in_ = in_
        self.out = out
        self.file = None

    @classmethod
    def _validate_id(cls, id_):
        """validates the given id value
        """
        if id_ is None:
            id_ = ''

        if not isinstance(id_, str):
            raise TypeError(
                '%(class)s.id should be a string, not %(id_class)s' %
                {
                    'class': cls.__name__,
                    'id_class': id_.__class__.__name__
                }
            )

        return id_

    @property
    def id(self):
        """returns the _id attribute value
        """
        return self._id

    @id.setter
    def id(self, id_):
        """setter for the _id attribute
        """
        self._id = self._validate_id(id_)

    def from_xml(self, xml_node):
        """Fills attributes with the given XML node

        :param xml_node: an xml.etree.ElementTree.Element instance
        """
        self.id = xml_node.attrib['id']
        self.start = float(xml_node.find('start').text)
        self.end = float(xml_node.find('end').text)
        self.name = xml_node.find('name').text
        self.enabled = xml_node.find('enabled').text == 'True'
        self.duration = float(xml_node.find('duration').text)
        self.in_ = float(xml_node.find('in').text)
        self.out = float(xml_node.find('out').text)

        f = File()
        file_tag = xml_node.find('file')
        f.from_xml(file_tag)

        self.file = f

    def to_xml(self, indentation=2, pre_indent=0):
        """returns an xml version of this Clip object
        """
        template = """%(pre_indent)s<clipitem id="%(id)s">
%(pre_indent)s%(indentation)s<end>%(end)s</end>
%(pre_indent)s%(indentation)s<name>%(name)s</name>
%(pre_indent)s%(indentation)s<enabled>%(enabled)s</enabled>
%(pre_indent)s%(indentation)s<start>%(start)s</start>
%(pre_indent)s%(indentation)s<in>%(in)s</in>
%(pre_indent)s%(indentation)s<duration>%(duration)s</duration>
%(pre_indent)s%(indentation)s<out>%(out)s</out>
%(file)s
%(pre_indent)s</clipitem>"""

        return template % {
            'id': self.id,
            'start': self.start,
            'end': self.end,
            'name': self.name,
            'enabled': self.enabled,
            'duration': self.duration,
            'in': self.in_,
            'out': self.out,
            'file': self.file.to_xml(indentation=indentation,
                                     pre_indent=pre_indent + indentation),
            'pre_indent': ' ' * pre_indent,
            'indentation': ' ' * indentation
        }


class File(PrevisBase, NameMixin, DurationMixin):
    """XML compatibility class for Sequencer
    """

    def __init__(self, duration=0, name='', pathurl=''):
        NameMixin.__init__(self, name=name)
        DurationMixin.__init__(self, duration=duration)
        self._pathurl = self._validate_pathurl(pathurl)

    @classmethod
    def _validate_pathurl(cls, pathurl):
        """validates the given pathurl value
        """
        if not isinstance(pathurl, str):
            raise TypeError(
                '%(class)s.pathurl should be a string, not '
                '%(pathurl_class)s' % {
                    'class': cls.__name__,
                    'pathurl_class': pathurl.__class__.__name__
                }
            )
        return pathurl

    @property
    def pathurl(self):
        """returns the _pathurl attribute
        """
        return self._pathurl

    @pathurl.setter
    def pathurl(self, pathurl):
        """setter for the pathurl property
        """
        self._pathurl = self._validate_pathurl(pathurl)

    def from_xml(self, xml_node):
        """Fills attributes with the given XML node

        :param xml_node: an xml.etree.ElementTree.Element instance
        """
        self.duration = float(xml_node.find('duration').text)
        self.name = xml_node.find('name').text
        self.pathurl = xml_node.find('pathurl').text

    def to_xml(self, indentation=2, pre_indent=0):
        """returns an xml version of this File object
        """
        template = """%(pre_indent)s<file>
%(pre_indent)s%(indentation)s<duration>%(duration)s</duration>
%(pre_indent)s%(indentation)s<name>%(name)s</name>
%(pre_indent)s%(indentation)s<pathurl>%(pathurl)s</pathurl>
%(pre_indent)s</file>"""
        return template % {
            'duration': self.duration,
            'name': self.name,
            'pathurl': self.pathurl,
            'pre_indent': ' ' * pre_indent,
            'indentation': ' ' * indentation
        }


class Sequencer(object):
    """The sequence instance.

    It is a manager that manages shot data. It is kind of the reflection of the
    Maya CameraSequencer.

    It is able to get Maya editorial XML and convert it to EDL.
    """

    @classmethod
    def create_shot_playblasts(cls, handle=10, show_ornaments=True):
        """creates the selected shot playblasts
        """
        import pymel.core

        shots = pymel.core.ls(sl=1, type=pymel.core.nt.Shot)
        #active_panel = pymel.core.playblast(activeEditor=1)

        path_template = os.path.join(
            pymel.core.workspace.name,
            'Outputs/Playblast/AllShots/'
        ).replace('\\', '/')

        filename_template = '%(scene)s_%(shot)s.mov'

        # template vars
        scene_name = os.path.basename(pymel.core.env.sceneName()).split('.')[0]

        for shot in shots:
            shot_name = shot.name()
            start_frame = shot.startFrame.get() - handle
            end_frame = shot.endFrame.get() + handle
            width = shot.wResolution.get()
            height = shot.hResolution.get()

            rendered_path = path_template % {}
            rendered_filename = filename_template % {
                'shot': shot_name,
                'scene': scene_name
            }

            movie_full_path = os.path.join(
                rendered_path,
                rendered_filename
            ).replace('\\', '/')

            pymel.core.playblast(
                fmt="qt",
                startTime=start_frame,
                endTime=end_frame,
                sequenceTime=1,
                forceOverwrite=1,
                filename=movie_full_path,
                clearCache=True,
                showOrnaments=show_ornaments,
                percent=100,
                wh=[width, height],
                offScreen=True,
                viewer=0,
                useTraxSounds=True,
                compression="PNG",
                quality=70
            )

    @classmethod
    def parse_xml(cls, path):
        """Parses XML file and returns a Sequence instance which reflects the
        whole timeline hierarchy.

        :param path: The path of the XML file
        :return: :class:`.Sequence`
        """
        if not isinstance(path, str):
            raise TypeError(
                'path argument in %s.parse_xml should be a string, not %s' %
                (cls.__name__, path.__class__.__name__)
            )

        from xml.etree import ElementTree
        try:
            tree = ElementTree.parse(path)
        except IOError:
            raise IOError('Please supply a valid path to an XML file!')

        root = tree.getroot()
        seq = Sequence()
        xml_seq = root.getchildren()[0]

        seq.from_xml(xml_seq)

        return seq

    @classmethod
    def to_xml(cls, seq, indentation=2, pre_indent=0):
        """Converts the given Sequence instance to an xml file

        :param seq: A :class:`.Sequence` instance
        :return: str
        """
        if not isinstance(seq, Sequence):
            raise TypeError(
                '"seq" argument in %s.to_xml should be an instance of'
                'anima.previs.Sequence, not %s' % (
                    cls.__name__, seq.__class__.__name__
                )
            )

        template = """<xmeml version="1.0">\n%(sequence)s\n</xmeml>\n"""

        return template % {
            'sequence': seq.to_xml(indentation=indentation,
                                   pre_indent=indentation + pre_indent)
        }

    @classmethod
    def to_edl(cls, seq):
        """returns an EDL for the given sequence

        :param seq: A :class:`.Sequence` instance
        """
        pass
