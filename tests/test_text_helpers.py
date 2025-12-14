import unittest
from src.text_helpers import extract_markdown_images, extract_markdown_links, text_to_textnodes
from src.textnode import TextType

class TestMarkdownExtraction(unittest.TestCase):

    # ------------------ IMAGE TESTS ------------------
    def test_single_image(self):
        text = "Here is an image ![alt text](https://example.com/image.png)"
        expected = [("alt text", "https://example.com/image.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "Images: ![first](http://a.com/1.png) and ![second](https://b.com/2.jpg)"
        expected = [("first", "http://a.com/1.png"), ("second", "https://b.com/2.jpg")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "No images here!"
        expected = []
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_image_with_special_chars(self):
        text = "Special ![alt-text_123](https://example.com/path/image-name_1.0.png)"
        expected = [("alt-text_123", "https://example.com/path/image-name_1.0.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_image_with_spaces_in_alt_text(self):
        text = "Check this ![my image here](https://example.com/img.png)"
        expected = [("my image here", "https://example.com/img.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_malformed_image_missing_alt(self):
        text = "Broken ![](https://example.com/image.png)"
        expected = [("", "https://example.com/image.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_malformed_image_missing_url(self):
        text = "Broken ![alt]()"
        expected = [("alt", "")]
        self.assertListEqual(extract_markdown_images(text), expected)

    # ------------------ LINK TESTS ------------------
    def test_single_link(self):
        text = "Visit [Boot.dev](https://www.boot.dev)"
        expected = [("Boot.dev", "https://www.boot.dev")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "Links: [Google](https://google.com) and [YouTube](https://youtube.com)"
        expected = [("Google", "https://google.com"), ("YouTube", "https://youtube.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "Just plain text"
        expected = []
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_link_with_special_chars(self):
        text = "Check [My Site](https://example.com/path/page?query=1&lang=en)"
        expected = [("My Site", "https://example.com/path/page?query=1&lang=en")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_link_with_spaces_in_text(self):
        text = "Link [Click here now](https://example.com)"
        expected = [("Click here now", "https://example.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_malformed_link_missing_text(self):
        text = "Broken [](https://example.com)"
        expected = [("", "https://example.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_malformed_link_missing_url(self):
        text = "Broken [link]()"
        expected = [("link", "")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_link_and_image_in_same_text(self):
        text = "See ![img](https://img.com/a.png) and [site](https://site.com)"
        expected_images = [("img", "https://img.com/a.png")]
        expected_links = [("site", "https://site.com")]
        self.assertListEqual(extract_markdown_images(text), expected_images)
        self.assertListEqual(extract_markdown_links(text), expected_links)


class TestTextToTextNodes(unittest.TestCase):
    
    def test_plain_text(self):
        text = "Just some plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_bold_text(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

    def test_italic_text(self):
        text = "This is _italic_ text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)

    def test_code_text(self):
        text = "Here is `code` snippet."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)

    def test_link_text(self):
        text = "Visit [Boot.dev](https://www.boot.dev) for more info."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "Boot.dev")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://www.boot.dev")

    def test_image_text(self):
        text = "Here is an image ![alt text](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[1].text, "alt text")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/image.png")

if __name__ == "__main__":
    unittest.main()
