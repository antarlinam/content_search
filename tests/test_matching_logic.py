import unittest
from app import app, match_content

class TestBusinessLogic(unittest.TestCase):

    def setUp(self):
        # Mock users data
        self.users = [
            {
                "name": "John Doe",
                "interests": [
                    {"type": "country", "value": "US", "threshold": 0.2},
                    {"type": "genre", "value": "Sci-Fi", "threshold": 0.5}
                ]
            },
            {
                "name": "Jane Smith",
                "interests": [
                    {"type": "country", "value": "UK", "threshold": 0.1}
                ]
            },
            {
                "name": "John Doe",
                "interests": [
                    {"type": "country", "value": "CA", "threshold": 0.3}
                ]
            }
        ]

        # Mock content data
        self.content = [
            {
                "id": "1",
                "title": "Interstellar",
                "content": "A science fiction film about space travel.",
                "tags": [
                    {"type": "country", "value": "US", "threshold": 0.25},
                    {"type": "content_category", "value": "Movies"}
                ]
            },
            {
                "id": "2",
                "title": "The Crown",
                "content": "A drama about the British royal family.",
                "tags": [
                    {"type": "country", "value": "UK", "threshold": 0.2},
                    {"type": "content_category", "value": "TV Shows"}
                ]
            },
            {
                "id": "3",
                "title": "Canadian Wildlife",
                "content": "A documentary about wildlife in Canada.",
                "tags": [
                    {"type": "country", "value": "CA", "threshold": 0.5},
                    {"type": "content_category", "value": "Documentaries"}
                ]
            }
        ]

    def test_name_matching_similar_names(self):
        """Test that similar names are suggested correctly."""
        matched_content = match_content(self.users, self.content)
        self.assertIn("john doe-US", matched_content)
        # Only assert if 'john doe-CA' is expected to have content matching.
        self.assertNotIn("john doe-CA", matched_content, "Expected no content for 'john doe-CA' as per mock data.")

    def test_country_implicit_match(self):
        """Test that matched results return the correct country."""
        matched_content = match_content(self.users, self.content)
        self.assertIn("john doe-US", matched_content)
        self.assertEqual(matched_content["john doe-US"]['user']['interests'][0]['value'], "US")
        # Ensure the absence if conditions are not met.
        self.assertNotIn("john doe-CA", matched_content, "Expected no content for 'john doe-CA' due to unmatched threshold.")

    def test_thresholds_correctly_handled(self):
        """Test that content matches are correctly based on threshold."""
        matched_content = match_content(self.users, self.content)
        # "Interstellar" has a threshold of 0.25 for "country" which is >= 0.2
        self.assertIn("Interstellar", [c['title'] for c in matched_content['john doe-US']['content']['Movies']])

    def test_content_categorization(self):
        """Test that results are categorized based on content category."""
        matched_content = match_content(self.users, self.content)
        self.assertIn("Movies", matched_content["john doe-US"]['content'])
        self.assertIn("TV Shows", matched_content["jane smith-UK"]['content'])
        # Checking if 'TV Shows' is not present for 'john doe-CA'
        self.assertNotIn("john doe-CA", matched_content)

    def test_multiple_results(self):
        """Test that multiple results are returned if multiple matches."""
        matched_content = match_content(self.users, self.content)
        self.assertEqual(len(matched_content["john doe-US"]['content']['Movies']), 1)
        self.assertEqual(len(matched_content["jane smith-UK"]['content']['TV Shows']), 1)

    def test_exclude_empty_categories(self):
        """Test that tables and headers without results are excluded."""
        matched_content = match_content(self.users, self.content)
        # "john doe-CA" should not have any TV Shows as per the mock data setup.
        self.assertNotIn("TV Shows", matched_content.get("john doe-CA", {}).get('content', {}))

if __name__ == '__main__':
    unittest.main()
