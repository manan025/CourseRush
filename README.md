# CourseRush
A python script that sends mail if a course is available for registration on SNU's ERP.

It has been checked to work on Pyton 3.14 with **GeckoDriver**. It may not work with Chrome.


## Installation & Setup
1. Install the required packages
```bash
uv add -r requirements.txt
```

To install geckodriver using homebrew (macOS):
```bash
brew install geckodriver
```

2. Create and initialize environment file
```bash
cp .env.example .env
```

3. Add the destination emails in [mail.py](mail.py) file. The `classes_not` variable in [main.py](main.py) contains the CCC that will not be monitored.



## Usage
1. Run the program
```bash
uv run main.py
```

## Features
- Headless Mode
- Inefficient but works
- Sends mail if a course is available for registration
- Can be used for multiple courses
