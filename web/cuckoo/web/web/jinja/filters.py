# Copyright (C) 2020 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from datetime import datetime

import dateutil.parser

from cuckoo.common.analyses import States as AnalysisStates
from cuckoo.common.task import States as TaskStates

def do_formatdatetime(value, fmt="%Y-%m-%d %H:%M"):
    return value.strftime(fmt)

def do_formatisodatetime(value, fmt="%Y-%m-%d %H:%M"):
    try:
        return do_formatdatetime(dateutil.parser.parse(value), fmt)
    except dateutil.parser.ParserError as e:
        raise ValueError(f"Invalid ISO format datetime '{value}'. {e}")

def do_humanstate(value):
    return AnalysisStates.to_human(value)

def do_taskstatehuman(value):
    return TaskStates.to_human(value)

filters = {
    "formatdatetime": do_formatdatetime,
    "formatisodatetime": do_formatisodatetime,
    "humanstate": do_humanstate,
    "taskstatehuman": do_taskstatehuman
}
