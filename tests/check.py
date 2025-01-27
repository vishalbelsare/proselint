"""Check that a check is working."""

from past.builtins import basestring
from unittest import TestCase
import os
import codecs


class Check(TestCase):
    """All tests inherit from Check."""

    __test__ = False

    def setUp(self):
        """Create a placeholder for setup procedure."""
        pass

    def tearDown(self):
        """Create a placeholder for teardown procedure."""
        from proselint.tools import close_cache_shelves
        close_cache_shelves()

    @property
    def this_check(self):
        """Create a placeholder for the specific check."""
        raise NotImplementedError

    def passes(self, lst):
        """Check if the test runs cleanly on the given text."""
        if isinstance(lst, basestring):
            lst = [lst]

        errors = []
        for text in lst:
            errors.append(self.this_check.check(text))

        return len(errors[0]) == 0

    def wpe_too_high(self):
        """Check whether the check is too noisy."""
        min_wpe = 50

        examples_dir = os.path.join(os.getcwd(), "tests", "corpus")
        examples = os.listdir(examples_dir)

        for example in examples:
            example_path = os.path.join(examples_dir, example)

            if ".DS_Store" in example_path:
                break

            # Compute the number of words per (wpe) error.
            with codecs.open(example_path, "r", encoding='utf-8') as f:
                text = f.read()
                num_errors = len(self.this_check.check(text))
                num_words = len(text)

            try:
                wpe = 1.0 * num_words / num_errors
            except ZeroDivisionError:
                wpe = float('Inf')

            # Make sure that
            assert wpe > min_wpe, \
                "{} has only {} wpe.".format(example, round(wpe, 2))
