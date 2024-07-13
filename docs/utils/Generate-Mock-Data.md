# Generate Mock data

Somethis is useful to have fake/mock data to test the behaviour of the app under different loads of data. With this script you can generate small, medium or large amounts of data.

## Command options

* `help`: for seeing the script usage in the terminal
* `small` | `medium` | `large`: the amount of data you want to generate

## Usage

1. Go to `Backend/`
2. Install app dependencies with `pip install -r requirements.txt`
3. Run `python -m app.tools.generate_mock_data [(help) | (small|medium|large)]`
