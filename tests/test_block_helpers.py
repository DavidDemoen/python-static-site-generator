import unittest

from src.block_helpers import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        self.assertEqual(
            markdown_to_blocks("Hello world"),
            ["Hello world"]
        )

    def test_two_blocks(self):
        self.assertEqual(
            markdown_to_blocks("Block one\n\nBlock two"),
            ["Block one", "Block two"]
        )

    def test_three_newlines(self):
        self.assertEqual(
            markdown_to_blocks("A\n\n\nB"),
            ["A", "B"]
        )

    def test_many_newlines(self):
        self.assertEqual(
            markdown_to_blocks("A\n\n\n\n\nB"),
            ["A", "B"]
        )

    def test_leading_newlines(self):
        self.assertEqual(
            markdown_to_blocks("\n\nBlock"),
            ["Block"]
        )

    def test_trailing_newlines(self):
        self.assertEqual(
            markdown_to_blocks("Block\n\n"),
            ["Block"]
        )

    def test_leading_and_trailing_newlines(self):
        self.assertEqual(
            markdown_to_blocks("\n\nBlock\n\n"),
            ["Block"]
        )

    def test_whitespace_block_removed(self):
        self.assertEqual(
            markdown_to_blocks("A\n\n   \n\nB"),
            ["A", "B"]
        )

    def test_tabs_and_spaces(self):
        self.assertEqual(
            markdown_to_blocks("A\n\n\t \n\nB"),
            ["A", "B"]
        )

    def test_single_newline_preserved(self):
        self.assertEqual(
            markdown_to_blocks("Line 1\nLine 2"),
            ["Line 1\nLine 2"]
        )

    def test_mixed_single_and_double_newlines(self):
        self.assertEqual(
            markdown_to_blocks("A\nB\n\nC\nD"),
            ["A\nB", "C\nD"]
        )


    def test_windows_newlines(self):
        self.assertEqual(
            markdown_to_blocks("A\r\n\r\nB"),
            ["A", "B"]
        )

    def test_mixed_newlines(self):
        self.assertEqual(
            markdown_to_blocks("A\r\n\nB"),
            ["A", "B"]
        )


    def test_empty_string(self):
        self.assertEqual(
            markdown_to_blocks(""),
            []
        )

    def test_only_newlines(self):
        self.assertEqual(
            markdown_to_blocks("\n\n\n"),
            []
        )

    def test_only_whitespace(self):
        self.assertEqual(
            markdown_to_blocks("   \n\n   "),
            []
        )

    def test_markdown_paragraphs(self):
        text = (
            "# Title\n"
            "\n"
            "Paragraph one\n"
            "still same paragraph\n"
            "\n\n"
            "- item 1\n"
            "- item 2\n"
        )

        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# Title",
                "Paragraph one\nstill same paragraph",
                "- item 1\n- item 2",
            ]
        )

    def test_idempotent(self):
        text = "A\n\nB\n\nC"
        blocks = markdown_to_blocks(text)
        rebuilt = "\n\n".join(blocks)

        self.assertEqual(
            markdown_to_blocks(rebuilt),
            blocks
        )


if __name__ == "__main__":
    unittest.main()