import nose.tools

import ckan.new_tests.helpers as helpers
import ckan.new_tests.factories as factories
import ckan.model as model

assert_equals = nose.tools.assert_equals
assert_not_equals = nose.tools.assert_not_equals
Resource = model.Resource


class TestResource(object):
    @classmethod
    def setup_class(cls):
        helpers.reset_db()

    def setup(self):
        model.repo.rebuild_db()

    def test_get_all_without_views_returns_all_resources_without_views(self):
        # Create resource with resource_view
        factories.ResourceView()

        expected_resources = [
            factories.Resource(format='format'),
            factories.Resource(format='other_format')
        ]

        resources = Resource.get_all_without_views()

        expected_resources_ids = [r['id'] for r in expected_resources]
        resources_ids = [r.id for r in resources]

        assert_equals(expected_resources_ids.sort(), resources_ids.sort())

    def test_get_all_without_views_accepts_list_of_formats_ignoring_case(self):
        factories.Resource(format='other_format')
        resource_id = factories.Resource(format='format')['id']

        resources = Resource.get_all_without_views(['FORMAT'])

        length = len(resources)
        assert length == 1, 'Expected 1 resource, but got %d' % length
        assert_equals([resources[0].id], [resource_id])
