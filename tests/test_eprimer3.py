#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_eprimer3.py

Test generation of ePrimer3 command-lines, primer file parsing and writing.

This test suite is intended to be run from the repository root using:

nosetests -v

(c) The James Hutton Institute 2017
Author: Leighton Pritchard

Contact:
leighton.pritchard@hutton.ac.uk

Leighton Pritchard,
Information and Computing Sciences,
James Hutton Institute,
Errol Road,
Invergowrie,
Dundee,
DD6 9LH,
Scotland,
UK

The MIT License

Copyright (c) 2017 The James Hutton Institute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import subprocess
import sys
import unittest

from diagnostic_primers import (eprimer3, config)

from nose.tools import assert_equal, raises


class TestCommands(unittest.TestCase):

    """Class defining tests of ePrimer3 command-line generation."""

    def setUp(self):
        """Set parameters for tests."""
        self.ep3_exe = 'eprimer3'
        self.datadir = os.path.join('tests', 'test_input', 'sequences')
        self.outdir = os.path.join('tests', 'test_output', 'eprimer3')
        self.targetdir = os.path.join('tests', 'test_targets', 'eprimer3')
        self.config = os.path.join('tests', 'test_input', 'config',
                                   'testprodigalconf.json')
        self.seqfile = os.path.join(self.datadir, "GCF_000011605.1.fasta")
        # Default values for ePrimer3 run - not modified by any tests,
        # defined in parsers.py
        self.ep3_defaults = {'ep_numreturn': 10,
                             'ep_osize': 20,
                             'ep_minsize': 18,
                             'ep_maxsize': 22,
                             'ep_opttm': 59,
                             'ep_mintm': 58,
                             'ep_maxtm': 60,
                             'ep_ogcpercent': 55,
                             'ep_mingc': 30,
                             'ep_maxgc': 80,
                             'ep_psizeopt': 100,
                             'ep_psizemin': 50,
                             'ep_psizemax': 150,
                             'ep_maxpolyx': 3,
                             'ep_osizeopt': 20,
                             'ep_ominsize': 13,
                             'ep_omaxsize': 30,
                             'ep_otmopt': 69,
                             'ep_otmmin': 68,
                             'ep_otmmax': 70,
                             'ep_ogcopt': 55,
                             'ep_ogcmin': 30,
                             'ep_ogcmax': 80,
                             }

    def test_eprimer3_exe(self):
        """ePrimer3 executable exists and runs."""
        cmd = "{0} --version".format(self.ep3_exe)
        result = subprocess.run(cmd, shell=sys.platform != "win32",
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True)
        # EMBOSS writes information out to STDERR
        assert_equal(result.stderr[:6], b'EMBOSS')

    def test_eprimer3_cmd(self):
        """ePrimer3 primer creation command builds correctly."""
        filestem = os.path.join(self.outdir,
                                os.path.split(self.seqfile)[-1])
        cmd = eprimer3.build_command(self.ep3_exe, self.seqfile,
                                     filestem, self.ep3_defaults)
        target = ' '.join(["eprimer3 -auto",
                           "-outfile=tests/test_output/eprimer3/GCF_000011605.1.fasta.eprimer3",
                           "-sequence=tests/test_input/sequences/GCF_000011605.1.fasta",
                           "-numreturn=10", "-osize=20", "-minsize=18", "-maxsize=22",
                           "-opttm=59", "-mintm=58", "-maxtm=60", "-ogcpercent=55",
                           "-mingc=30", "-maxgc=80", "-maxpolyx=3", "-psizeopt=100",
                           "-prange=50-150", "-osizeopt=20", "-ominsize=13",
                           "-omaxsize=30", "-otmopt=69", "-otmmin=68", "-otmmax=70",
                           "-ogcopt=55", "-ogcmin=30", "-ogcmax=80"])
        assert_equal(str(cmd), target)

    def test_eprimer3_cmds(self):
        """ePrimer3 primer creation commands build with no errors."""
        pdpc = config.PDPCollection()
        pdpc.from_json(self.config)
        clines = eprimer3.build_commands(pdpc, self.ep3_exe, self.outdir,
                                         self.ep3_defaults)
