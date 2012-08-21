"""
Test the MustacheRendererFactory class.
"""

import os
import unittest
from pyramid import testing
from pystache.renderer import Renderer
import pyramid_mustache
from pyramid_mustache.renderer import MustacheRendererFactory
from .dummy import DummyPackage, DummyConfig, DummyInfo


class TestRenderer(unittest.TestCase):

    """
    Test the MustacheRendererFactory class.
    """

    def setUp(self):
        """Set up the test data."""
        here = os.path.abspath(os.path.dirname(__file__))
        self.settings = {'mustache.search': os.path.join(here, 'templates')}

        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        self.config.registry.settings = self.settings
        self.request.registry = self.config.registry
        
        self.template_simple = 'simple'
        self.info_simple = DummyInfo({
            'name': self.template_simple + '.mustache',
            'registry': self.config.registry})

        self.template_partial = 'partial_parent'
        self.info_partial = DummyInfo({
            'name': self.template_partial + '.mustache',
            'registry': self.config.registry})

    def test_init(self):
        """Test initializing the renderer object."""
        pyramid_mustache.session.configure(self.settings)        
        factory = MustacheRendererFactory(self.info_simple)
        renderer = pyramid_mustache.session.get_renderer()
        self.assertEqual(factory.renderer.search_dirs, renderer.search_dirs,
            'factory.renderer is invalid')
        self.assertEqual(factory.template, self.template_simple,
            'factory.template is invalid')

    def test_call_simple(self):
        """Test rendering a simple template."""
        pyramid_mustache.session.configure(self.settings)
        data = {'renderer': 'Mustache'}
        expected = "Rendered by %s.\n" % data['renderer']
        factory = MustacheRendererFactory(self.info_simple)
        self.assertEqual(factory(data, None), expected,
            'failed to render simple template')

    def test_call_partial(self):
        """Test rendering a template with partials."""
        pyramid_mustache.session.configure(self.settings)
        data = {}
        expected = "Include a partial.\nThis is a partial.\n"
        factory = MustacheRendererFactory(self.info_partial)
        self.assertEqual(factory(data, None), expected,
            'failed to render template with partials')

