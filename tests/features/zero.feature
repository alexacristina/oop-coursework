Feature: Convert Markdown text to HTML text
    In order to see the result of my markdown document
    As a FAF-121 student 
    I want to convert markdown document to HTML document.

    Scenario: Convert Markdown File to HTML file
        Given I load the markdown file 'input.md' with the output 'myoutput.html'
        When I convert it to HTML
        Then I see the result of an HTML file similar to 'output.html'.

    Scenario: Convert Markdown File from URL to HTML file similar to the one from URL
        Given I load the markdown file from URL: 'https://gist.githubusercontent.com/minivan/f29e2759c44d13e39b5b/raw/7bc948fc89d467db05d879e61ac09a7f70f75362/input.md'
        When I convert the file to HTML
        Then I see a result like the one at the URL: 'https://gist.githubusercontent.com/minivan/a2de5b21a649d7ad0f7f/raw/1398320f80223fe7e666cddd0774b5f71a7cf53e/output.html'