from django.forms import Widget
from django.test import TestCase
from ..forms import SensitiveDataMixin


class SensitiveDataMixinTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up basic test.
        class TestWidget(SensitiveDataMixin, Widget):
            pass

        self.sensitive_widget = TestWidget(attrs={'name': 'foo'})
        self.widget = TestWidget()


    def test_mixin_removes_name_attribute_from_form_widget(self):
        '''
        Ensure that the Mixin replaces the 'name' attribute of the Widget that
        it extends. This is required as part of PCI compliance.
        '''
        attributes = self.sensitive_widget.build_attrs()

        self.assertNotIn('name', attributes)


    def test_mixin_does_nothing_if_name_attribute_is_not_present_in_form_widget(self):
        '''
        Ensure that the Mixin does nothing if the 'name' attribute is not
        present in the Widget that it extends.
        '''
        attributes = self.widget.build_attrs()

        self.assertNotIn('name', attributes)
