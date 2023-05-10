## Instructions

This code was written in Python 3.11.3.
Use a fresh Python 3.11 environment for the below instructions.
1. From the root directory, run `pip install -r requirements.txt`
2. To run unit tests, run `pytest`
3. To start the app server run `uvicorn app.main:app`
4. You can then 
   - either navigate to the endpoints required in the specification using your web browser
   - query the endpoints using cURL e.g. `curl localhost:8000/api/titles/1`

## Notes

Given a little more time I would
- Restrict the possible values for `title_class` to the two options as currently it is possible for it to be any string.
- Add handling for invalid input e.g. for passing something other than `desc` or `asc` for the order.
- Add unit tests for the invalid input cases, currently there are only tests for successful use cases.
- Add unit tests for multiple column sorting and ordering.