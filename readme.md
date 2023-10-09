# Semi-automatic Log Book Poster

## Dependencies:
- Python 3.10
- Selenium
- Pandas
- WebDriver (e.g., ChromeDriver)

## Usage:
1. Fill data.csv
2. Adjust Chrome Driver Path
3. Win + R and ```chrome --remote-debugging-port=8888``` (you may adjust the debugging port)
4. Open enrichment.apps.binus.ac.id -> Enrichment Activity -> Log Book -> Select Month
5. If you work on Saturday, change the 'off' variable to False
6. Run Script ```python.exe main.py```
7. Wait until finished, check the submissions, click submit on the web