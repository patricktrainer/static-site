import unittest
from unittest.mock import Mock, patch
from your_module import render  # replace 'your_module' with the actual name of your module

class TestRender(unittest.TestCase):
    @patch('your_module.get_template')  # replace 'your_module' with the actual name of your module
    def test_render(self, mock_get_template):
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = '<html>Rendered Template</html>'
        mock_get_template.return_value = mock_template
        expected_html = '<html>Rendered Template</html>'
        kwargs = {'key1': 'value1', 'key2': 'value2'}

        # Act
        actual_html = render('template', **kwargs)

        # Assert
        mock_get_template.assert_called_once()
        mock_template.render.assert_called_once_with(**kwargs)
        self.assertEqual(expected_html, actual_html)

if __name__ == '__main__':
    unittest.main()
