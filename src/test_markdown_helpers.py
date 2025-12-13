import unittest

from markdown_helpers import extract_markdown_links, extract_markdown_images

class TestMdImageHelper(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_two_messagse(self):
        matches = extract_markdown_images(
            "This is text with an first ![image](https://i.imgur.com/zjjcJKZ.png) and second ![image2](https://i.imgur.com/zjjcJKZ.pdf)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2","https://i.imgur.com/zjjcJKZ.pdf")])
    def test_no_images(self):
        matches = extract_markdown_images(
            "This text has no images at all"
        )
        self.assertListEqual([], matches)

    def test_ignore_links_when_finding_images(self):
        matches = extract_markdown_images(
            "A [link](https://example.com) but no images"
        )
        self.assertListEqual([], matches)

    def test_malformed_image_missing_url(self):
        matches = extract_markdown_images(
            "Broken image ![image](https://example.com"
        )
        self.assertListEqual([], matches)


class TestMdLinkHelper(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_extract_two_links(self):
        matches = extract_markdown_links(
            "Links: [one](https://one.com) and [two](https://two.com)"
        )
        self.assertListEqual(
            [
                ("one", "https://one.com"),
                ("two", "https://two.com"),
            ],
            matches
        )

    def test_ignore_images_when_finding_links(self):
        matches = extract_markdown_links(
            "![image](https://example.com/img.png) and a [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_no_links(self):
        matches = extract_markdown_links(
            "This text has no links"
        )
        self.assertListEqual([], matches)

    def test_malformed_link_missing_closing_paren(self):
        matches = extract_markdown_links(
            "Broken [link](https://example.com"
        )
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()
    