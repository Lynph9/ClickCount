# ClickCount

A small Tkinter desktop tool that listens for global **left mouse clicks**, counts
them in batches of 200, plays a success bell each time 200 is reached, and then
resets the batch counter while incrementing the total number of completed
batches.

## Requirements
- Python 3.10+
- `tkinter` (ships with most Python distributions)
- `pynput` for the global mouse listener

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Run the counter and keep clicking your mouse as usual:

```bash
python click_counter.py
```

- Only **left** button presses are counted.
- Every 200 clicks triggers the system bell, resets the current batch back to 0,
  and adds +1 to the "Completed batches" total in the UI.
- Close the window to stop the listener.
