import unittest
from src.html_helpers import markdown_to_html_node  

class TestMarkdownToHTMLNode(unittest.TestCase):

    #Paragraph Tester
    def test_single_paragraph(self):
        md = "This is a single paragraph."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is a single paragraph.</p></div>"
        )

    def test_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p></div>"
        )

    def test_paragraph_with_inline_markdown(self):
        md = "This is **bold** and this is _italic_ and this is `code`."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bold</b> and this is <i>italic</i> and this is <code>code</code>.</p></div>"
        )

    def test_paragraph_with_line_breaks_inside_block(self):
        md = "Line 1 of paragraph\nLine 2 of paragraph"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Line 1 of paragraph Line 2 of paragraph</p></div>"
        )

    def test_paragraph_with_leading_and_trailing_whitespace(self):
        md = "   Paragraph with whitespace around   "
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Paragraph with whitespace around</p></div>"
        )

    def test_paragraphs_with_empty_lines(self):
        md = "\n\nFirst paragraph.\n\n\nSecond paragraph.\n\n"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>First paragraph.</p><p>Second paragraph.</p></div>"
        )

    def test_paragraph_with_special_characters(self):
        md = "Special characters: <, >, & should appear as-is in HTML"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Special characters: <, >, & should appear as-is in HTML</p></div>"
        )
    
    # Quote Tests
    def test_single_line_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_multi_line_quote(self):
        md = "> This is a quote\n> that spans multiple lines"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote that spans multiple lines</blockquote></div>"
        )

    def test_quote_with_inline_markdown(self):
        md = "> This is **bold**\n> and _italic_"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is <b>bold</b> and <i>italic</i></blockquote></div>"
        )

    def test_quote_with_code_inline(self):
        md = "> Use `code` here"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>Use <code>code</code> here</blockquote></div>"
        )

    def test_quote_with_leading_and_trailing_whitespace(self):
        md = "   > Quote with whitespace   "
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>Quote with whitespace</blockquote></div>"
        )

    def test_multiple_separate_quotes(self):
        md = "> First quote\n\n> Second quote"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>First quote</blockquote><blockquote>Second quote</blockquote></div>"
        )

    def test_invalid_quote_mixed_lines(self):
        md = "> This is a quote\nThis is not"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>> This is a quote This is not</p></div>"
        )

    def test_quote_with_special_characters(self):
        md = "> < & > should appear as-is"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>< & > should appear as-is</blockquote></div>"
        )
    
    # Unordered List Tests

    def test_single_item_unordered_list(self):
        md = "- Single item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Single item</li></ul></div>"
        )

    def test_multiple_items_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_unordered_list_with_inline_markdown(self):
        md = "- **Bold item**\n- _Italic item_\n- `Code item`"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>Bold item</b></li><li><i>Italic item</i></li><li><code>Code item</code></li></ul></div>"
        )

    def test_unordered_list_with_leading_whitespace(self):
        md = "   - Item with leading space"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item with leading space</li></ul></div>"
        )

    def test_multiple_separate_unordered_lists(self):
        md = "- First list item\n- Second list item\n\n- Another list item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>First list item</li><li>Second list item</li></ul><ul><li>Another list item</li></ul></div>"
        )

    def test_invalid_unordered_list_line_breaks(self):
        md = "- Item 1\nNot a list item\n- Item 2"
        node = markdown_to_html_node(md)
        # Line that does not start with '-' should break the list; fallback to paragraph
        self.assertEqual(
            node.to_html(),
            "<div><p>- Item 1 Not a list item - Item 2</p></div>"
        )

    def test_unordered_list_with_special_characters(self):
        md = "- < & > should appear as-is\n- * bullet marker"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>< & > should appear as-is</li><li>* bullet marker</li></ul></div>"
        )

    def test_unordered_list_with_mixed_markers_fails(self):
        md = "- Item 1\n* Item 2\n+ Item 3"
        node = markdown_to_html_node(md)
        # Mixed markers should be treated as invalid or as separate blocks depending on implementation
        self.assertEqual(
            node.to_html(),
            "<div><p>- Item 1 * Item 2 + Item 3</p></div>"
        )

    #Ordered List Tests

    def test_single_item_ordered_list(self):
        md = "1. First item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First item</li></ol></div>"
        )

    def test_multiple_items_ordered_list(self):
        md = "1. Item 1\n2. Item 2\n3. Item 3"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>"
        )

    def test_ordered_list_with_inline_markdown(self):
        md = "1. **Bold item**\n2. _Italic item_\n3. `Code item`"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li><b>Bold item</b></li><li><i>Italic item</i></li><li><code>Code item</code></li></ol></div>"
        )

    def test_ordered_list_with_leading_whitespace(self):
        md = "   1. Item with leading space"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>Item with leading space</li></ol></div>"
        )

    def test_multiple_separate_ordered_lists(self):
        md = "1. First item\n2. Second item\n\n1. Another list item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First item</li><li>Second item</li></ol><ol><li>Another list item</li></ol></div>"
        )

    def test_invalid_ordered_list_numbering_fails(self):
        md = "1. Item 1\n3. Item 2\n4. Item 3"
        node = markdown_to_html_node(md)
        # Non-consecutive numbers => fallback to paragraph
        self.assertEqual(
            node.to_html(),
            "<div><p>1. Item 1 3. Item 2 4. Item 3</p></div>"
        )

    def test_ordered_list_with_special_characters(self):
        md = "1. < & > should appear as-is\n2. * bullet marker"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>< & > should appear as-is</li><li>* bullet marker</li></ol></div>"
        )
    def test_single_line_code_block(self):
            md = "```\nprint('Hello World')\n```"
            node = markdown_to_html_node(md)
            self.assertEqual(
                node.to_html(),
                "<div><pre><code>print('Hello World')</code></pre></div>"
            )

    def test_multi_line_code_block(self):
            md = """```
    def add(a, b):
        return a + b
    ```"""
            node = markdown_to_html_node(md)
            self.assertEqual(
                node.to_html(),
                "<div><pre><code>def add(a, b):\n    return a + b</code></pre></div>"
            )

    def test_code_block_with_inline_markdown_inside(self):
            md = """```
    This **should** not be parsed as bold
    Neither _italic_ nor `code`
    ```"""
            node = markdown_to_html_node(md)
            self.assertEqual(
                node.to_html(),
                "<div><pre><code>This **should** not be parsed as bold\nNeither _italic_ nor `code`</code></pre></div>"
            )

    def test_code_block_empty(self):
            md = "```\n```"
            node = markdown_to_html_node(md)
            self.assertEqual(
                node.to_html(),
                "<div><pre><code></code></pre></div>"
            )
    
    # Header tests
    def test_single_line_headers(self):
        for i in range(1, 7):
            md = f"{'#' * i} Header level {i}"
            node = markdown_to_html_node(md)
            self.assertEqual(
                node.to_html(),
                f"<div><h{i}>Header level {i}</h{i}></div>"
            )

    def test_header_with_trailing_whitespace(self):
        md = "### Header with spaces   "
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h3>Header with spaces</h3></div>"
        )

    def test_header_with_inline_markdown(self):
        md = "## **Bold Header**"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h2><b>Bold Header</b></h2></div>"
        )


if __name__ == "__main__":
    unittest.main()