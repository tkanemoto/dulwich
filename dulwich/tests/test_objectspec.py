# test_objectspec.py -- tests for objectspec.py
# Copyright (C) 2014 Jelmer Vernooij <jelmer@samba.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your option) any later version of
# the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Tests for revision spec parsing."""

# TODO: Round-trip parse-serialize-parse and serialize-parse-serialize tests.


from dulwich.objects import (
    Blob,
    )
from dulwich.objectspec import (
    parse_object,
    parse_commit_range,
    parse_ref,
    parse_refs,
    parse_reftuple,
    parse_reftuples,
    )
from dulwich.repo import MemoryRepo
from dulwich.tests import (
    TestCase,
    )
from dulwich.tests.utils import (
    build_commit_graph,
    )


class ParseObjectTests(TestCase):
    """Test parse_object."""

    def test_nonexistent(self):
        r = MemoryRepo()
        self.assertRaises(KeyError, parse_object, r, "thisdoesnotexist")

    def test_blob_by_sha(self):
        r = MemoryRepo()
        b = Blob.from_string(b"Blah")
        r.object_store.add_object(b)
        self.assertEqual(b, parse_object(r, b.id))


class ParseCommitRangeTests(TestCase):
    """Test parse_commit_range."""

    def test_nonexistent(self):
        r = MemoryRepo()
        self.assertRaises(KeyError, parse_commit_range, r, "thisdoesnotexist")

    def test_commit_by_sha(self):
        r = MemoryRepo()
        c1, c2, c3 = build_commit_graph(r.object_store, [[1], [2, 1],
            [3, 1, 2]])
        self.assertEqual([c1], list(parse_commit_range(r, c1.id)))


class ParseRefTests(TestCase):

    def test_nonexistent(self):
        r = {}
        self.assertRaises(KeyError, parse_ref, r, b"thisdoesnotexist")

    def test_head(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual(b"refs/heads/foo", parse_ref(r, b"foo"))

    def test_full(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual(b"refs/heads/foo", parse_ref(r, b"refs/heads/foo"))


class ParseRefsTests(TestCase):

    def test_nonexistent(self):
        r = {}
        self.assertRaises(KeyError, parse_refs, r, [b"thisdoesnotexist"])

    def test_head(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual([b"refs/heads/foo"], parse_refs(r, [b"foo"]))

    def test_full(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual([b"refs/heads/foo"], parse_refs(r, b"refs/heads/foo"))


class ParseReftupleTests(TestCase):

    def test_nonexistent(self):
        r = {}
        self.assertRaises(KeyError, parse_reftuple, r, r, b"thisdoesnotexist")

    def test_head(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual((b"refs/heads/foo", b"refs/heads/foo", False),
            parse_reftuple(r, r, b"foo"))
        self.assertEqual((b"refs/heads/foo", b"refs/heads/foo", True),
            parse_reftuple(r, r, b"+foo"))
        self.assertEqual((b"refs/heads/foo", b"refs/heads/foo", True),
            parse_reftuple(r, {}, b"+foo"))

    def test_full(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual((b"refs/heads/foo", b"refs/heads/foo", False),
            parse_reftuple(r, r, b"refs/heads/foo"))


class ParseReftuplesTests(TestCase):

    def test_nonexistent(self):
        r = {}
        self.assertRaises(KeyError, parse_reftuples, r, r,
            [b"thisdoesnotexist"])

    def test_head(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual([(b"refs/heads/foo", b"refs/heads/foo", False)],
            parse_reftuples(r, r, [b"foo"]))

    def test_full(self):
        r = {b"refs/heads/foo": "bla"}
        self.assertEqual([(b"refs/heads/foo", b"refs/heads/foo", False)],
            parse_reftuples(r, r, b"refs/heads/foo"))
