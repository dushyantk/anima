# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Anima Istanbul
#
# This module is part of anima-tools and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
"""Utilities for UI stuff
"""
import os
import logging

from anima.utils import StalkerThumbnailCache


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from anima.ui.lib import QtCore, QtGui


def get_icon(icon_name):
    """Returns an icon from ui library
    """
    here = os.path.abspath(os.path.dirname(__file__))
    images_path = os.path.join(here, 'images')
    icon_full_path = os.path.join(images_path, icon_name)
    return QtGui.QIcon(icon_full_path)


def clear_thumbnail(gview):
    """Clears the thumbnail for the given QGraphicsView

    :param gview: The QGraphicsView instance
    """

    if not gview:
        return

    # clear the graphics scene in case there is no thumbnail
    scene = gview.scene()
    if not scene:
        scene = QtGui.QGraphicsScene(gview)
        gview.setScene(scene)

    scene.clear()


def update_gview_with_task_thumbnail(task, gview, login, password):
    """Updates the given QGraphicsView with the given Task thumbnail

    :param task: A
      :class:`~stalker.models.task.Task` instance

    :param gview: A QtGui.QGraphicsView instance
    """
    from stalker import Task

    if not isinstance(task, Task) or \
            not isinstance(gview, QtGui.QGraphicsView):
        # do nothing
        logger.debug('task is not a stalker.models.task.Task instance')
        return

    # get the thumbnail full path
    full_path = None
    if task.thumbnail:
        # use the cache system to get the thumbnail
        if 'SPL' in task.thumbnail.full_path:
            full_path = StalkerThumbnailCache.get(
                task.thumbnail.full_path,
                login,
                password
            )
        else:
            # try to get it as a normal file
            repo = task.project.repository
            full_path = os.path.join(
                repo.path,
                task.thumbnail.full_path
            )
            if not os.path.exists(full_path):
                full_path = None
    else:
        logger.debug('there is no thumbnail')
        # try to get the thumbnail from parents
        for parent in task.parents:
            if parent.thumbnail:
                # use the cache system to get the thumbnail
                if 'SPL' in parent.thumbnail.full_path:
                    full_path = StalkerThumbnailCache.get(
                        parent.thumbnail.full_path,
                        login,
                        password
                    )
                else:
                    # try to get it as a normal file
                    repo = parent.project.repository
                    full_path = os.path.join(
                        repo.path,
                        parent.thumbnail.full_path
                    )
                    if not os.path.exists(full_path):
                        full_path = None
                logger.debug('found parent thumbnail at: %s' % full_path)
                break

    if full_path:
        update_gview_with_image_file(
            full_path,
            gview
        )


def update_gview_with_image_file(image_full_path, gview):
    """updates the QGraphicsView with the given image
    """

    if not isinstance(gview, QtGui.QGraphicsView):
        return

    clear_thumbnail(gview)

    if image_full_path != "":
        image_full_path = os.path.normpath(image_full_path)
        image_format = os.path.splitext(image_full_path)[-1].replace('.', '').upper()
        logger.debug("creating pixmap from: %s" % image_full_path)

        # size = conf.thumbnail_size
        # width = size[0]
        # height = size[1]
        size = gview.size()
        width = size.width()
        height = size.height()
        logger.debug('width: %s' % width)
        logger.debug('height: %s' % height)

        if os.path.exists(image_full_path):
            pixmap = QtGui.QPixmap(image_full_path, format=image_format).scaled(
                width, height,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            # pixmap = QtGui.QPixmap(image_full_path, format='JPG')

            scene = gview.scene()
            scene.addPixmap(pixmap)


def upload_thumbnail(entity, thumbnail_source_full_path):
    """Uploads the given thumbnail for the given entity

    :param entity: An instance of :class:`~stalker.models.entity.SimpleEntity`
      or a derivative.

    :param str thumbnail_source_full_path: A string which is showing the path
      of the thumbnail image
    """

    # get width height
    # width = size[0]
    # height = size[0]

    thumbnail_full_path = entity.thumbnail.full_path

    # upload the chosen image to the repo, overwrite any image present
    # create the dirs
    try:
        os.makedirs(os.path.split(thumbnail_full_path)[0])
    except OSError:
        # dir exists
        pass

    # instead of copying the item
    # just render a resized version to the output path
    pixmap = QtGui.QPixmap(thumbnail_source_full_path, format='JPG')#.scaled(
    # width, height,
    # QtCore.Qt.KeepAspectRatio,
    # QtCore.Qt.SmoothTransformation
    # )
    # now render it to the path
    # pixmap.save(
    #     thumbnail_full_path,
    #     conf.thumbnail_format,
    #     conf.thumbnail_quality
    # )
    pixmap.save(thumbnail_full_path, 'jpg', 85)


def choose_thumbnail(parent):
    """shows a dialog for thumbnail upload
    """
    # get a file from a FileDialog
    thumbnail_full_path = QtGui.QFileDialog.getOpenFileName(
        parent, "Choose Thumbnail",
        os.path.expanduser("~"),
        "Image Files (*.png *.jpg *.bmp)"
    )

    if isinstance(thumbnail_full_path, tuple):
        thumbnail_full_path = thumbnail_full_path[0]

    return thumbnail_full_path


def render_image_from_gview(gview, image_full_path):
    """renders the gview scene to an image at the given full path
    """
    assert isinstance(gview, QtGui.QGraphicsView)
    scene = gview.scene()
    # there should be only one item
    items = scene.items()
    if items:
        pixmapItem = items[0]
        pixmap = pixmapItem.pixmap()
        try:
            os.makedirs(os.path.split(image_full_path)[0])
        except OSError:
            # dir exists
            pass

        pixmap.save(
            image_full_path
        )
