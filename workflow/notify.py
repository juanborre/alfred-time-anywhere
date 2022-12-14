#!/usr/bin/env python3
# This module relies on Notificator created by Vítor Galvão
# See https://github.com/vitorgalvao/notificator

"""
Post notifications via the macOS Notification Center.

The main API is a single function, :func:`~workflow.notify.notify`.

It works by copying a simple application to your workflow's cache
directory.
"""

import os
import subprocess

from . import workflow

_wf = None
_log = None


#: Available system sounds from System Preferences > Sound > Sound Effects
SOUNDS = (
    "Basso",
    "Blow",
    "Bottle",
    "Frog",
    "Funk",
    "Glass",
    "Hero",
    "Morse",
    "Ping",
    "Pop",
    "Purr",
    "Sosumi",
    "Submarine",
    "Tink",
)


def wf():
    """Return Workflow object for this module.

    Returns:
        workflow.Workflow: Workflow object for current workflow.
    """
    global _wf
    if _wf is None:
        _wf = workflow.Workflow()
    return _wf


def log():
    """Return logger for this module.

    Returns:
        logging.Logger: Logger for this module.
    """
    global _log
    if _log is None:
        _log = wf().logger
    return _log


def notify(title="", text="", sound=""):
    """Post notification via Notify.app helper.

    Args:
        title (str, optional): Notification title.
        text (str, optional): Notification body text.
        sound (str, optional): Name of sound to play.

    Raises:
        ValueError: Raised if both ``title`` and ``text`` are empty.

    Returns:
        bool: ``True`` if notification was posted, else ``False``.
    """
    if text == "":
        raise ValueError("A message is mandatory.")

    notificator = os.path.join(os.path.dirname(__file__), "notificator")
    retcode = subprocess.run(
        [notificator, "--title", title, "--message", text, "--sound", sound], check=True
    ).returncode

    if retcode == 0:
        return True

    log().error("Notificator exited with status %s", retcode)
    return False
