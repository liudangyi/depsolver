import unittest

from depsolver.package \
    import \
        Package
from depsolver.requirement \
    import \
        Requirement, RequirementParser
from depsolver.requirement_parser \
    import \
        Equal, GEQ, LEQ
from depsolver.version \
    import \
        Version

V = Version.from_string

class TestRequirementParser(unittest.TestCase):
    def test_simple(self):
        parser = RequirementParser()

        r_requirements = [Requirement("numpy", [GEQ("1.3.0")])]
        requirements = parser.parse("numpy >= 1.3.0")
        self.assertEqual(r_requirements, list(requirements))

        r_requirements = [Requirement("numpy", [GEQ("1.3.0"),
                                                LEQ("2.0.0")])]
        requirements = parser.parse("numpy >= 1.3.0, numpy <= 2.0.0")
        self.assertEqual(r_requirements, list(requirements))

        r_requirements = [Requirement("numpy", [Equal("1.3.0")])]
        requirements = parser.parse("numpy == 1.3.0")
        self.assertEqual(r_requirements, list(requirements))

        r_requirements = [Requirement("numpy", [Equal("1.3.0"),
                                                Equal("1.4.0")])]
        requirements = parser.parse("numpy == 1.3.0, numpy == 1.4.0")
        self.assertEqual(r_requirements, list(requirements))

    def test_repr(self):
        requirement_string = "numpy >= 1.3.0, numpy <= 2.0.0"
        parser = RequirementParser()
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), requirement_string)

    def test_from_string(self):
        requirement_string = "numpy >= 1.3.0, numpy <= 2.0.0"
        parser = RequirementParser()
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(numpy_requirement, Requirement.from_string(requirement_string))

    def test_matches(self):
        parser = RequirementParser()

        numpy_requirement = list(parser.parse("numpy >= 1.3.0, numpy <= 2.0.0"))[0]
        self.assertFalse(numpy_requirement.match(Package("numpy", V("1.2.0"))))
        self.assertTrue(numpy_requirement.match(Package("numpy", V("1.4.0"))))
        self.assertTrue(numpy_requirement.match(Package("numpy", V("1.5.0"))))

        numpy_requirement = list(parser.parse("numpy == 1.3.0"))[0]
        self.assertFalse(numpy_requirement.match(Package("numpy", V("1.2.0"))))
        self.assertTrue(numpy_requirement.match(Package("numpy", V("1.3.0"))))
        self.assertFalse(numpy_requirement.match(Package("numpy", V("1.4.0"))))
        self.assertFalse(numpy_requirement.match(Package("numpy", V("1.5.0"))))

        numpy_requirement = list(parser.parse("numpy >= 1.3.0"))[0]
        self.assertFalse(numpy_requirement.match(Package("numpy", V("1.2.0"))))
        self.assertTrue(numpy_requirement.match(Package("numpy", V("1.4.0"))))
        self.assertTrue(numpy_requirement.match(Package("numpy", V("1.5.0"))))

        numpy_requirement = list(parser.parse("numpy <= 1.3.0"))[0]
        self.assertTrue(numpy_requirement.match(Package("numpy", V("1.2.0"))))
        self.assertFalse(numpy_requirement.match(Package("numpy", V("1.4.0"))))
        self.assertFalse(numpy_requirement.match(Package("numpy", V("1.5.0"))))
